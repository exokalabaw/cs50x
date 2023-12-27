window.onload = () => {
    const formchecks = [...document.getElementsByClassName("quizitem")];
    const tbutton = document.getElementById("checkscore");
    const rbtn = document.getElementById("reviewBtn");
    tbutton.addEventListener("click", checkScore);
    rbtn.addEventListener("click", reviewQuestions);
    let submitactive = false;
    formchecks.forEach((x)=>{
        if(x.type == "text"){
            x.addEventListener("input",checkInput);
        }else{
            x.addEventListener("change",checkInput);
        }

    });
    function checkInput(e){
        // console.log(e.target.name);
        let emptyfound = false
        answerkey.forEach((y)=>{
            let qn = y.question_number;
            if(y.qt == "multiple_choice"){
                // console.log('this is multi')
                let selected = document.querySelector("input[name='question"+qn+"']:checked");

                if (!selected){

                  emptyfound = true;
                }
            }else{
                // console.log('this is not multi')
                let tf = document.querySelector("input[name='question"+qn+"']");
                // console.log("value length of "+qn+" : "+tf.value.length)
                if(!tf.value.length){
                    emptyfound = true
                }
            }


        });
        if(emptyfound && submitactive){
            tbutton.disabled = true;
            submitactive = false;
        }else if(!emptyfound && !submitactive){
            tbutton.disabled = false;
            submitactive = true;
        }
    }

    function checkScore(){
        let perfectscore = answerkey.length;
        let userscore = 0;
        let rv = document.getElementById("resultviewer")
        answerkey.forEach((y)=>{
            let qn = y.question_number;
            let ans = y.answer;
            let type = y.qt;
            if(y.qt == "multiple_choice"){
                let selected = document.querySelector("input[name='question"+qn+"']:checked");

                if(selected.value == 1){
                    userscore ++;
                }
            }else{
                let tf = document.querySelector("input[name='question"+qn+"']");
                tfv = tf.value
                ans.forEach((d)=>{
                    if (tfv == d){
                        userscore ++;
                    }
                })
            }

        });
        rv.innerHTML = "<h5>Your score is :</h5> <br/><h3>"+userscore +"/"+perfectscore+"</h3>";
        const allfields = [...document.getElementsByClassName("quizitem")]
        allfields.forEach((x)=>{
            x.disabled = true;
        })
        tbutton.remove();
        document.getElementById("retake").classList.remove("hidden");

    }
    function reviewQuestions(){

        answerkey.forEach((y)=>{
            let qn = y.question_number;
            let ans = y.answer;
            let type = y.qt;
            let parent;
            if(y.qt == "multiple_choice"){
                let selected = document.querySelector("input[name='question"+qn+"']:checked");
                let label = document.querySelector("label[for='"+selected.id+"']");
                parent = selected.parentElement;
                let answer;
                ans.forEach((a)=>{
                    if(a.correct == 1){
                        answer = a.pa;
                    }
                })
                if(selected.value == 1){

                    label.classList.add("text-success");
                    // console.log("id of selected" +selected.id);
                    parent.insertAdjacentHTML( 'beforeend'," <p class='text-success'>correct!</p>");
                }else{
                    label.classList.add("text-danger");
                    parent.insertAdjacentHTML( 'beforeend'," <div><p class='mt-2 mb-0 text-danger'>incorrect.</p><small><a class='showanswerlink'>show answer</a></small><br/><small class='text-success hidden' id='shownanswer" + selected.id + "'>The answer is "+answer+"</small></div>");
                }

            }else{
                let tf = document.querySelector("input[name='question"+qn+"']");
                tfv = tf.value;
                dangerous = true;
                parent = tf.parentElement;
                answersashtm = "";
                ans.forEach((d)=>{
                    answersashtm = answersashtm + d + ", ";
                    if (tfv == d){
                        dangerous = false;

                    }
                })
                if(dangerous){
                    tf.classList.add("text-danger")
                    parent.insertAdjacentHTML( 'beforeend'," <div><p class='mt-2 mb-0 text-danger'>incorrect.</p><small><a class='showanswerlink'>show answer</a></small><br/><small class='text-success hidden' >Possible answers are "+ answersashtm +"</small></div>");
                }else{
                    tf.classList.add("text-success")
                    parent.insertAdjacentHTML( 'beforeend'," <p class='mt-2 text-success'>correct!</p>");
                }

            }

        });
        linkBinders = [...document.getElementsByClassName("showanswerlink")]
        linkBinders.forEach((lb)=>{
            lb.addEventListener("click", showthisone);
        })

    }
    function showthisone(l){
        const lp = l.target.parentElement.parentElement;
        smallsuccess = [...lp.getElementsByClassName("text-success")];
        smallsuccess[0].classList.remove("hidden");
        l.target.remove();
    }
}
