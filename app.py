from flask import Flask, request
app = Flask(__name__)
HTML="""
<h2>BMI Calculator</h2>
<form method="post">
    Weight (kg):<input type="number" step="0.1" name="weight" required><br><br>
    Height (m):<input type="number" step="0.01" name="height" required><br><br>
    <button type="submit">Calculate</button>
</form>
<h3>{result}</h3>
"""
@app.route("/",methods=["GET","POST"])
def bmi():
    result="" 
    if request.method=="POST":
        w=float(request.form["weight"])
        h=float(request.form["height"])
        bmi=round(w/h*h,2)
        if bmi<18.5:
            cat="underweight"
        elif bmi<25:
            cat="normal"
        elif bmi<30:
            cat="overweight"
        else:
            cat="obese"
        result=f"BMI: {bmi}({cat})"
    return HTML.format(result=result)
if __name__ == "__main__":
    app.run(debug=True)