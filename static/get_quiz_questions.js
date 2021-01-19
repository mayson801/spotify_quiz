function shuffle(array) {
    var currentIndex = array.length, temporaryValue, randomIndex

    while(0 !==currentIndex){
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex-=1;

        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
    }
return array
}

function printarray(array) {
    console.log("the length of array is " + array.length)
    for( var i=0; i< array.length; i++){
    console.log(array[i]["id"])
    }
}
function get_correct_answers(data){
    var answers = []
    var shuffled_array = shuffle(data)
    for (var i = 0; i< 10; i++){
        answers.push(shuffled_array[i])
    }
return answers
}

function get_possible_answers(correct_answer,array){
list_of_answers = []
list_of_answers.push(correct_answer)
array = shuffle(array)
i=0
    while (list_of_answers.length < 4){
        if (array[i] == correct_answer){
            i=i+1;
        }
        else{
            list_of_answers.push(array[i])
            i=i+1
        }
    }
list_of_answers = shuffle(list_of_answers)
return list_of_answers
}

