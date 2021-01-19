function main(data_object){
    var data_object = JSON.parse(data_JSON);

    var i = 0;
    while (i < data_object.length){
        console.log(i.toString())
        var image_node = document.createElement("IMG");
        image_node.setAttribute("src",data_object[i]['artist_image']);

        var node = document.createElement("h1");
        var textnode = document.createTextNode(data_object[i]['artist_name']);

        var node1 = document.createElement("p");
        var textnode1 = document.createTextNode(data_object[i]['followers/description']);


        node.appendChild(textnode);
        node1.appendChild(textnode1);

        document.getElementById("row_"+ i.toString()).appendChild(image_node);
        document.getElementById("row_"+ i.toString()).appendChild(node);
        document.getElementById("row_"+ i.toString()).appendChild(node1);

        i = i+1
    }
}
function mouse_over_boxes(id, type){
    if (type == "in"){
    document.getElementById(id).style.backgroundColor = 'rgba(0,0,255,0.5)'
    }
    else{
    document.getElementById(id).style.backgroundColor = 'rgba(0,0,255,0)'
    }}

function on_click_function(data_object,button_num){
    var chosen_id = data_object[button_num]['artist_id'];
        $.ajax({
            url: "quiz_page.html",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({chosen_id})
        }).done(function(data) {
            console.log(data);
        });
        window.location = "/loading";
}

