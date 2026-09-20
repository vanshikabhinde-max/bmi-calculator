from flask import Flask, request
app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box} 
  body{margin:0; min-height:100vh; font-family:Poppins,sans-serif;
    background: linear-gradient(120deg,#89f7fe 0%, #66a6ff 100%);
    display:flex; align-items:center; justify-content:center; padding:20px;}
  .card{width:420px; background:rgba(255,255,255,.9); backdrop-filter: blur(12px);
    border-radius:28px; padding:30px; box-shadow:0 25px 50px rgba(0,0,0,.2);}
  h2{text-align:center; margin:0; color:#1e293b;}
  .sub{text-align:center; color:#64748b; font-size:13px; margin-bottom:22px}
  .field{margin-bottom:18px}
  .top{display:flex; justify-content:space-between; align-items:center}
  label{font-weight:600; font-size:13px; color:#334155}
  .val{font-weight:700; color:#6366f1; background:#eef2ff; padding:4px 10px; border-radius:20px; font-size:13px}
  input[type=range]{width:100%; accent-color:#6366f1; margin-top:10px}
  input[type=number]{width:100%; padding:12px 14px; border:1.5px solid #e2e8f0; border-radius:12px; margin-top:8px}
  .gauge{width:160px; height:160px; border-radius:50%; margin:20px auto;
    display:grid; place-items:center; background: conic-gradient(#e2e8f0 0deg, #e2e8f0 360deg);
    transition: .8s ease; position:relative}
  .gauge-inner{width:130px; height:130px; background:white; border-radius:50%;
    display:grid; place-items:center; text-align:center; box-shadow:inset 0 0 10px rgba(0,0,0,.05)}
  #bmiNum{font-size:32px; font-weight:800; color:#1e293b; line-height:1}
  #bmiCat{font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px}
  button{width:100%; padding:14px; border:none; border-radius:14px; font-weight:700; font-size:15px;
    background:linear-gradient(90deg,#6366f1,#8b5cf6); color:white; cursor:pointer;
    box-shadow:0 10px 20px rgba(99,102,241,.3); transition:.2s}
  button:active{transform:scale(.98)}
  .result{margin-top:16px; padding:14px; border-radius:14px; text-align:center; font-weight:600; display:none}
  .tips{font-size:12px; color:#64748b; text-align:center; margin-top:12px}
  .scale{display:flex; gap:6px; margin-top:14px}
  .scale div{flex:1; height:6px; border-radius:10px; background:#f1f5f9}
  .scale div.active{transform:scaleY(1.6)}
</style>
</head>
<body>
<div class="card">
  <h2>⚖️ Body Balance</h2>
  <p class="sub">Interactive BMI Calculator</p>
  
  <form method="post" id="form">
    <div class="field">
      <div class="top"><label>Weight (kg)</label><span class="val" id="wVal">68 kg</span></div>
      <input type="range" id="wRange" min="30" max="150" step="0.5" value="68">
      <input type="number" step="0.1" name="weight" id="weight" value="68" required hidden>
    </div>
    <div class="field">
      <div class="top"><label>Height (m)</label><span class="val" id="hVal">1.75 m</span></div>
      <input type="range" id="hRange" min="1.2" max="2.2" step="0.01" value="1.75">
      <input type="number" step="0.01" name="height" id="height" value="1.75" required hidden>
    </div>

    <div class="gauge" id="gauge">
      <div class="gauge-inner">
        <div><div id="bmiNum">--</div><div id="bmiCat">BMI</div></div>
      </div>
    </div>

    <div class="scale">
      <div id="s1" title="Underweight"></div>
      <div id="s2" title="Normal"></div>
      <div id="s3" title="Overweight"></div>
      <div id="s4" title="Obese"></div>
    </div>

    <button type="submit">Calculate & Save</button>
    <div class="result" id="serverResult">__SERVER_RESULT__</div>
    <p class="tips">💡 Drag sliders for live preview. Click Calculate to lock it.</p>
  </form>
</div>

<script>
  const wRange=document.getElementById('wRange'), hRange=document.getElementById('hRange');
  const weight=document.getElementById('weight'), height=document.getElementById('height');
  const wVal=document.getElementById('wVal'), hVal=document.getElementById('hVal');
  const bmiNum=document.getElementById('bmiNum'), bmiCat=document.getElementById('bmiCat');
  const gauge=document.getElementById('gauge');
  const s=[document.getElementById('s1'),document.getElementById('s2'),document.getElementById('s3'),document.getElementById('s4')];

  function update(){
    const w=parseFloat(wRange.value), h=parseFloat(hRange.value);
    weight.value=w; height.value=h;
    wVal.textContent=w+' kg'; hVal.textContent=h+' m';
    const bmi = w/(h*h);
    if(!h) return;
    bmiNum.textContent=bmi.toFixed(1);
    let cat,color,deg;
    if(bmi<18.5){cat='Underweight'; color='#3b82f6'; deg=bmi*6; s.forEach((e,i)=>e.style.background=i==0?color:'#f1f5f9');}
    else if(bmi<25){cat='Normal'; color='#22c55e'; deg=70 + (bmi-18.5)*8; s.forEach((e,i)=>e.style.background=i==1?color:'#f1f5f9');}
    else if(bmi<30){cat='Overweight'; color='#f59e0b'; deg=120 + (bmi-25)*10; s.forEach((e,i)=>e.style.background=i==2?color:'#f1f5f9');}
    else{cat='Obese'; color='#ef4444'; deg=170 + Math.min(bmi-30,20)*3; s.forEach((e,i)=>e.style.background=i==3?color:'#f1f5f9');}
    bmiCat.textContent=cat; bmiCat.style.color=color;
    gauge.style.background=`conic-gradient(${color} ${deg}deg, #e2e8f0 ${deg}deg)`;
  }
  wRange.addEventListener('input',update); hRange.addEventListener('input',update);
  update();

  // show server result if exists
  const sr=document.getElementById('serverResult');
  if(sr.textContent.trim()!==''){
    sr.style.display='block';
    const txt=sr.textContent.toLowerCase();
    if(txt.includes('under')){sr.style.background='#eff6ff'; sr.style.color='#1d4ed8'}
    else if(txt.includes('normal')){sr.style.background='#f0fdf4'; sr.style.color='#15803d'}
    else if(txt.includes('over')){sr.style.background='#fefce8'; sr.style.color='#a16207'}
    else{sr.style.background='#fef2f2'; sr.style.color='#b91c1c'}
  }
</script>
</body>
</html>
"""

@app.route("/", methods=["GET","POST"])
def bmi_route():
    server_result = ""
    if request.method == "POST":
        w = float(request.form["weight"])
        h = float(request.form["height"])
        bmi_val = round(w / (h*h), 2)
        if bmi_val < 18.5: cat="underweight"
        elif bmi_val < 25: cat="normal"
        elif bmi_val < 30: cat="overweight"
        else: cat="obese"
        server_result = f"✅ Saved — BMI: {bmi_val} ({cat})"

    return HTML_PAGE.replace("__SERVER_RESULT__", server_result)

if __name__ == "__main__":
    app.run(debug=True)