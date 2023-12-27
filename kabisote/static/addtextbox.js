window.onload = () => {
    const tfield = document.getElementById("question");
    const addanother = document.getElementById("addanother");
    const savebtn = document.getElementById("savequestion");
    const aa = document.getElementById("addanother");
    const xers = [...document.getElementsByClassName("xout")];
    xers.forEach((kl)=>{
        kl.addEventListener("click", destroy);
    })
    const answerfields = [...document.getElementsByClassName("answerfield")];
    answerfields.forEach((af)=>{
        af.addEventListener("input", checkInput);
    })
    document.getElementById("addanother").onclick = clicker;

    tfield.addEventListener("input", checkInput);
    var namepopulated = false;
    var anspopulated = false;
    var submitactive = false;


    function checkInput(e,d){
        cid = e.target.id;
        cl = escape(e.target.value);
        cl = cl.length;


        if(cl >= 1){
            if(!submitactive){
                let formchecks = document.getElementsByClassName("formcheck");
                let arr = [...formchecks];
                let keepdisable = false;
                let al = arr.length;

                console.log('arr length ' + arr.length);
                for( let i = 0; i < arr.length; i++){
                    console.log('what is this doing : ' + arr[i].value)

                    if(!arr[i].value){
                        if(d && i == arr.length - 1){

                        }else{
                            keepdisable = true;
                            break;
                        }

                    }
                }
                if (!keepdisable){
                    savebtn.disabled = false;
                    submitactive = true;
                }
            }


        }else{
            if(submitactive){
                savebtn.disabled = true;
                submitactive = false;
            }

        }

    }

    function destroy(e){
        let todestroy = e.target.id;
        todestroy = todestroy.slice(1)
        const dest = document.getElementById(todestroy);
        checkInput(e,1);
        dest.remove();
    }

    function clicker(){
        // const elementcount = document.getElementsByClassName("answerfield").length
        const uniqueid = Date.now()
        const newelement = `<div  id="${uniqueid}"class='mb-3 tfield'>
            <input autocomplete='off' autofocus class='form-control answerfield formcheck' id='answer${uniqueid}' name='answer${uniqueid}' placeholder='Alternate answer' type='text'>
            <a class='xout' id="d${uniqueid}" >-</a>
        </div>`
        tfields.insertAdjacentHTML( 'beforeend', newelement);
        const newfield = document.getElementById(`answer${uniqueid}`);
        const destroylink = document.getElementById(`d${uniqueid}`);
        destroylink.addEventListener("click", destroy);
        newfield.addEventListener("input", checkInput);
        savebtn.disabled = true;
        submitactive = false;
    }



}




