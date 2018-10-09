const truth_table_request = new XMLHttpRequest();
const rendered_truth_table = new XMLHttpRequest();
var b = true;

document.getElementById("generate").addEventListener("click", function () {
    var input = document.getElementById("expression").value;
    if(input.length < 1) {
        alert("Please fill in a logical expression before generating a tree");
    } else {
        json = JSON.stringify({"expression": input});
        truth_table_request.open("POST", "/create_truth_table", true);
        truth_table_request.setRequestHeader("Content-Type", "application/json");
        truth_table_request.send(json);
    }
});

truth_table_request.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200){
        var json = JSON.parse(this.responseText);
        var error = json['error'];
        if(error) {
            alert(json["error"]);
        } else {
            if('image' in json) {
                var img_container = document.getElementById("graph-image");
                img_container.src = "../static/images/" + json["image"];
                b = true;
            } else { b = false; }
            rendered_truth_table.open("POST", "/render_table", true);
            rendered_truth_table.setRequestHeader("Content-Type", "application/json");
            rendered_truth_table.send(JSON.stringify({
                "table": json["table"],
                "identification": json["identification"],
                "normalization": json["normalization"]}));
        }
    }
};

rendered_truth_table.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
        var img_container = document.getElementById("graph-image");
        if(b) { img_container.style.display = "block"; }
        else { img_container.style.display = "none"; }
        var table_container = document.getElementById("truth-table");
        table_container.innerHTML = this.responseText;
    }
};

document.getElementById("simplify").addEventListener("click", function () {
    var input = document.getElementById("expression").value;
    if(input.length < 1) {
        alert("Please fill in a logical expression before generating a tree");
    } else {
        json = JSON.stringify({"expression": input});
        truth_table_request.open("POST", "/simplify", true);
        truth_table_request.setRequestHeader("Content-Type", "application/json");
        truth_table_request.send(json);
    }
});
