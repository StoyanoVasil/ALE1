const graph_request = new XMLHttpRequest();

document.getElementById("generate").addEventListener("click", function () {
    var input = document.getElementById("expression").value;
    if(input.length < 1) {
        alert("Please fill in a logical expression before generating a tree");
    } else {
        json = JSON.stringify({"expression": input});
        graph_request.open("POST", "/expression_image", true);
        graph_request.setRequestHeader("Content-Type", "application/json");
        graph_request.send(json);
    }
});

graph_request.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200){
        var json = JSON.parse(this.responseText);
        var img_name = json['image'];
        if(img_name) {
            var img_container = document.getElementById("graph-image");
            img_container.style.display = "block";
            img_container.src = "../static/images/" + img_name;
        } else {
            alert(json["error"]);
        }
    }
};
