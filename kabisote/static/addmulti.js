window.onload = () => {
    const tfield = document.getElementById("question");
    const addanother = document.getElementById("addanother");
    const firstfield = document.getElementById("answer1");
    const secondfield = document.getElementById("answer2");
    const savebtn = document.getElementById("savequestion");
    const aa = document.getElementById("addanother");
    const multiradios = [...document.getElementsByClassName("multiradio")];
    multiradios.forEach((rad)=>{
        rad.addEventListener("click",checkInput)
    })
    const additionals = [...document.getElementsByClassName("nondefault")];
    if(additionals){
        additionals.forEach((dagdag)=>{
            dagdag.addEventListener("input",checkInput)
        })
    }

    document.getElementById("addanother").onclick = clicker;
    firstfield.addEventListener("input", checkInput);
    tfield.addEventListener("input", checkInput);
    secondfield.addEventListener("input", checkInput);
    var submitactive = false;


    function checkInput(e,d){
        cid = e.target.id;
        cl = escape(e.target.value);
        cl = cl.length;
        type = e.type
        if(cl>= 1 || type == "change"){
            console.log('tttt')
            //if submit is not enabled and the current field is not empty
            if(!submitactive){
                let arr = [...document.getElementsByClassName("formcheck")];
                let mrarr = [...document.getElementsByClassName("multiradio")];

                let keepdisable = false;
                for( let i = 0; i < arr.length; i++){

                    if(!arr[i].value){
                        if(d && i == arr.length -1){

                        }else{
                            keepdisable = true;
                            break;
                        }


                    }
                }
                //check if no tickboxes are ticked
                let allblank  = true;

                mrarr.forEach((eto)=>{
                    console.log('eto ba? ')
                    if(eto.checked){
                        allblank = false;
                        console.log('may laman')
                    }else{
                        console.log('walang laman')
                    }
                });





                if(allblank){
                    keepdisable = true
                }
                if (!keepdisable){
                    savebtn.disabled = false;
                    submitactive = true;
                }

            }

        }else{
            if (submitactive){
                savebtn.disabled = true;
                submitactive = false;
            }
        }
        // if the length of the input is empty, disable submit X
        // if it's not empty, if enabled is true, do nothing
        // if it's not empty and disabled is true, iterate through all inastances to check if there's another empty field. if yes, do nothing
        // if there are no other empty fields, enable submit

    }



    function clicker(){
        const uniqueid = Date.now()
        const newelement = `<div id="${uniqueid}" class="mb-3 tfield">
            <input autocomplete="off" autofocus class="form-control mb-2 formcheck" id="answer${uniqueid}" name="answer${uniqueid}" placeholder="Answer" type="text">
            <input id="cb${uniqueid}" type="radio"  name="answer" value="${uniqueid}" class="multiradio">
            <label for="cb${uniqueid}">Correct answer</label></br>
            <a class='xout' id="d${uniqueid}" >-</a>
        </div>`
        tfields.insertAdjacentHTML( 'beforeend', newelement);
        const newfield = document.getElementById(`answer${uniqueid}`);

        newfield.addEventListener("input", checkInput);
        savebtn.disabled = true;
        const destroylink = document.getElementById(`d${uniqueid}`);
        destroylink.addEventListener("click", destroy);
        submitactive = false;
        initradios();
    }
    function destroy(e){
        let todestroy = e.target.id;
        todestroy = todestroy.slice(1)
        let dest = document.getElementById(todestroy);
        let radiocheck = [...dest.getElementsByClassName("multiradio")]
        radiocheck = radiocheck[0].checked;
        if (radiocheck){

            let tocheck = [...document.getElementsByClassName("tfield")]
            d = tocheck[0].getElementsByClassName("multiradio")
            console.log('tocheck' + d[0].checked)
            d[0].checked = true;
        }
        dest.remove();
        checkInput(e,1)
    }

    function initradios(){
        const radio = document.querySelectorAll('input[name="cb"]');
        const xout = [...document.getElementsByClassName('xout')];
        if(xout){
            xout.forEach((x)=>{
                x.addEventListener("click", destroy);
            })
        }
         for(let o = 0; o < radio.length; o++){
            radio[o].addEventListener("change", checkInput)
        }
    }

    initradios()

}





