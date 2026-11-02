#!/usr/bin/env python3
"""Build RU/UK/EN search intent data from distinct real Russian queries."""
import csv,json,os,re
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"Processing"/"selected_sources_for_3_languages.csv"
READY=ROOT/"Ready"
CLASSES=["INFORMATIONAL","COMMERCIAL","TRANSACTIONAL","NAVIGATIONAL","LOCAL","MIXED","UNKNOWN"]
LANGS=["ru","uk","en"]
MODELS={"uk":"Helsinki-NLP/opus-mt-ru-uk","en":"Helsinki-NLP/opus-mt-ru-en"}
UNKN=re.compile(r"фыв|ыва|йцук|цукен|qwert|asdf|zxcv|qweq|asdasd|testtest|апрол|пролд|abcabc|123123|ячсм",re.I)
BADUNKN=re.compile(r"купить|цена|клавиатур|раскладк|перевод|цвет|рубл|доллар|евро|песня|погода|сколько|инструкц|сайт",re.I)
BADLOCAL=re.compile(r"песня|песню|песни|слушать|смотреть|скачать|ты не бойся|ведь я рядом|рядом с тобой|айпи адрес|ip адрес|погода|осадки|фильм|боевые действия",re.I)

def load():
    result=defaultdict(list)
    with SOURCE.open(encoding="utf-8-sig",newline="") as f:
        for r in csv.DictReader(f,delimiter=";"):
            cl=r["class"]
            if cl not in CLASSES:continue
            q=r["source_ru"].strip()
            if not q:continue
            if cl=="LOCAL" and (BADLOCAL.search(q) or q in {"адрес","маршрут","рядом","как добраться"}):continue
            if cl=="UNKNOWN" and (not UNKN.search(q) or BADUNKN.search(q)):continue
            if cl=="MIXED" and (len(q.split())<4 or q=="купить отзывы"):continue
            result[cl].append({"q":q,"freq":int(r["exact_frequency"]),"assigned":r["target_assignment"]})
    return result

def groups(data):
    output={}
    for cl in CLASSES:
        rows=data.get(cl,[])
        seen=set()
        for lang in LANGS:
            pool=[r for r in rows if r["assigned"]==lang]
            pool.extend(r for r in rows if r["assigned"]!=lang)
            group=[]
            for row in pool:
                key=re.sub(r"\s+"," ",row["q"].lower().replace("ё","е"))
                if key in seen:continue
                group.append(row);seen.add(key)
                if len(group)==300:break
            output[(cl,lang)]=group
    return output

def translate(items,lang):
    if not items:return []
    from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
    import torch
    model_id=MODELS[lang]
    tokenizer=AutoTokenizer.from_pretrained(model_id)
    model=AutoModelForSeq2SeqLM.from_pretrained(model_id)
    model.eval()
    torch.set_num_threads(max(1,min(3,os.cpu_count() or 2)))
    out=[]
    with torch.inference_mode():
        for i in range(0,len(items),16):
            part=items[i:i+16]
            tokens=tokenizer(part,return_tensors="pt",padding=True,truncation=True,max_length=128)
            pred=model.generate(**tokens,num_beams=1,max_new_tokens=96)
            out.extend(tokenizer.batch_decode(pred,skip_special_tokens=True))
            if i%480==0:print(lang,"translated",min(i+16,len(items)),"of",len(items),flush=True)
    return out

RU="йцукенгшщзхъфывапролджэячсмитьбю"
EN="qwertyuiop[]asdfghjkl;'zxcvbnm,."
KEYS=dict(zip(RU,EN))
UKTRANS=str.maketrans({"ы":"і","э":"є","ъ":"ї","ё":"й"})
def noise(q,lang):
    if lang=="uk":return q.translate(UKTRANS)
    if lang=="en":return "".join(KEYS.get(s,s) for s in q.lower())
    return q

def save_csv(path,fields,rows):
    with path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter=";",extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def main():
    source=load()
    chosen=groups(source)
    todo={lang:[] for lang in ("uk","en")}
    for lang in ("uk","en"):
        for cl in CLASSES:
            if cl!="UNKNOWN":
                todo[lang].extend(r["q"] for r in chosen[(cl,lang)])
    translations={lang:translate(todo[lang],lang) for lang in ("uk","en")}
    cursor=Counter()
    dataset=[];provenance=[]
    report={"target_rows":6300,"source":"Bukvarix processed exports","source_collected_at":None,
            "models":MODELS,"counts":{},"warnings":[]}
    for cl in CLASSES:
        report["counts"][cl]={}
        for lang in LANGS:
            group=chosen[(cl,lang)]
            report["counts"][cl][lang]={"rows":len(group),"target":300,"missing":300-len(group)}
            for r in group:
                q=r["q"]
                if lang=="ru":text=q;method="original_ru"
                elif cl=="UNKNOWN":text=noise(q,lang);method="keyboard_adaptation_not_translation"
                else:
                    text=translations[lang][cursor[lang]]
                    cursor[lang]+=1
                    method="machine_translation_"+MODELS[lang]
                text=re.sub(r"\s+"," ",text.strip())
                if not text:raise ValueError("Empty query in "+cl+":"+lang)
                dataset.append({"text":text,"language":lang,"collected_at":"","class_example":cl})
                provenance.append({"class":cl,"language":lang,"text":text,"source_ru":q,
                                   "source_exact_frequency":r["freq"],"method":method,
                                   "needs_review":lang!="ru" or cl=="UNKNOWN"})
    READY.mkdir(exist_ok=True)
    save_csv(READY/"queries_multilingual.csv",["text","language","collected_at","class_example"],dataset)
    save_csv(READY/"queries_provenance.csv",["class","language","text","source_ru","source_exact_frequency","method","needs_review"],provenance)
    report["total_rows"]=len(dataset)
    report["missing_rows"]=6300-len(dataset)
    report["warnings"]=[
        "Generated translations require manual QA, especially entities, slang and ambiguous intent.",
        "UNKNOWN cannot be semantically translated: keyboard-mash adaptation is explicitly marked.",
        "Source collection date unknown; collected_at is deliberately blank.",
        "RU sources are taken from the user-provided Bukvarix export; UK/EN translations are derived, not observed searches.",
        "Missing source queries are not fabricated; consult missing_rows and class counts."
    ]
    (READY/"quality_report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    (READY/"README.md").write_text(
        "# Multilingual search-intent dataset\n\n"
        "queries_multilingual.csv follows example/queries_example.csv (text;language;collected_at;class_example).\n\n"
        "queries_provenance.csv maps every translated row to its original Russian Bukvarix phrase and exact frequency.\n\n"
        "quality_report.json provides class/language counts and shortfalls.\n\n"
        "Ukrainian and English rows are OPUS-MT translations and are not observed search queries; human review required.\n\n"
        "UNKNOWN strings are keyboard adapted rather than translated. Original collection dates are unknown and are left blank.\n",
        encoding="utf-8"
    )
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
