from flask import Flask, render_template, request

app = Flask(__name__)

def generate_TAC(code):
    tac_code = []
    lines = code.strip().split("\n")
    label_counter = 0  
    stack = []  

    for line in lines:
        line = line.strip()

       
        if "=" in line and "if" not in line and "while" not in line:
            parts = line.split("=")

           
            if len(parts) > 2:
                left = parts[0].strip()
                right = "=".join(parts[1:]).strip()  
            else:
                left, right = parts[0].strip(), parts[1].strip()

            tac_code.append(f"{left} = {right}")

        elif "if" in line and "else" not in line:
            condition = line.replace("if", "").replace("(", "").replace(")", "").strip()
            false_label = f"L{label_counter}"
            label_counter += 1
            tac_code.append(f"if {condition} == false goto {false_label}")
            stack.append(false_label)  

        elif "else" in line:
            end_label = f"L{label_counter}"
            label_counter += 1
            tac_code.append(f"goto {end_label}")
            if stack:
                tac_code.append(f"{stack.pop()}:")  
            stack.append(end_label)  

    
        elif "while" in line:
            condition = line.replace("while", "").replace("(", "").replace(")", "").strip()
            start_label = f"L{label_counter}"
            label_counter += 1
            false_label = f"L{label_counter}"
            label_counter += 1
            tac_code.append(f"{start_label}: if {condition} == false goto {false_label}")
            stack.append((start_label, false_label))  

      
        elif "}" in line:
            if stack:
                top = stack.pop()
                if isinstance(top, tuple):  
                    start_label, false_label = top
                    tac_code.append(f"goto {start_label}")  
                    tac_code.append(f"{false_label}:")  
                else: 
                    tac_code.append(f"{top}:")  

    return "\n".join(tac_code)


@app.route("/", methods=["GET", "POST"])
def home():
    tac_output = ""
    if request.method == "POST":
        input_code = request.form["input_code"]
        tac_output = generate_TAC(input_code)
    return render_template("index.html", tac_output=tac_output)

if __name__ == "__main__":
    app.run(debug=True)
