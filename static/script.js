function openTab(tab) {
    document.querySelectorAll(".tab").forEach(t => t.style.display="none");
    document.getElementById(tab).style.display="block";
}

async function summarize(){
let file=document.getElementById("brdFile").files[0];
let text=await file.text();

let res=await fetch("/summarize",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});
let data=await res.json();
document.getElementById("summaryOutput").innerText=data.summary;
}

async function generate(){
let text=document.getElementById("reqText").value;

let res=await fetch("/generate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});
let data=await res.json();

document.getElementById("qaOutput").innerText=JSON.stringify(data.data,null,2);
alert("Saved: "+data.file);
}

async function review(){
let dev=document.getElementById("devFile").files[0];
let qa=document.getElementById("qaFile").files[0];

let fd=new FormData();
fd.append("dev",dev);
fd.append("qa",qa);

let res=await fetch("/review",{method:"POST",body:fd});
let data=await res.json();

document.getElementById("missingOutput").innerText=
"Missing in QA:\n"+data.missing_in_qa.join("\n")+
"\n\nMissing in Dev:\n"+data.missing_in_dev.join("\n")+
"\n\nMissing Categories QA:\n"+data.missing_cat_qa.join(", ");
}