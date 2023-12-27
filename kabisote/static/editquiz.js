window.onload = () => {



    function reorder(){
        cheverlies = [...document.getElementsByClassName("cheverly")]
        tfield = [...document.getElementsByClassName("tfield")]
        tfieds = document.getElementById("tfields");
        fieldsform = document.getElementById("orderfields");
        temps = [...document.getElementsByClassName("tempfield")]
        temps.forEach((h)=>{
            h.remove();
        });

        var d = 1;
        tfield.forEach((k)=>{
            let classlist = k.classList;
            let ordernumber = k.dataset.orderNumber;
            let itemid = k.dataset.itemId;
            let addinput = "<input type='checkbox' checked class='hidden tempfield' id="+itemid+" name="+itemid+" value="+ordernumber+">";
            fieldsform.insertAdjacentHTML('afterbegin', addinput);
            console.log("classlist is initially: "+classlist);
            if (d == 1 && !classlist.contains('first')){
                classlist.add('first');
            }else if (d == tfield.length && !classlist.contains('last')){
                classlist.add('last');
            }else if(d > 1 && d < tfield.length){
                classlist.remove('first')
                classlist.remove('last')
            }
            console.log("classlist became: "+classlist);
            d++;
        });
        cheverlies.forEach((c)=>{

            c.addEventListener("click", ()=>{cheverloo(c.parentElement.dataset.orderNumber, c.dataset.direction)})
        })
    }
    reorder();


    function cheverloo(on, dd){
        tfieds = document.getElementById("tfields");
        let lower = null;
        let higher = null;
        on = parseInt(on)
        //higher and lower pertains to weight
        //up and down pertains to the direction the div is going
        if(dd == "up"){
            higher = on;
            lower = on - 1;

        }else{
            higher = on + 1;
            lower = on;
        }
        lmnthigher = document.querySelector("[data-order-number='"+higher+"']");
        lmntlower = document.querySelector("[data-order-number='"+lower+"']")
        console.log("direction is "+dd+", " + higher +" goes up to " + lower)


        tfields.insertBefore(lmnthigher, lmntlower);
        let temp = lmnthigher.dataset.orderNumber;
        lmnthigher.setAttribute('data-order-number', lmntlower.dataset.orderNumber);
        lmntlower.setAttribute('data-order-number', temp);
        const clone = tfields.cloneNode(true);
        var tcontainer = document.getElementById("tcontainer");
        tcontainer.innerHTML = "";
        tcontainer.appendChild(clone);
        var ordersaver = document.getElementById("ordersaver");
        if (ordersaver.classList.contains("hidden")){
            ordersaver.classList.remove("hidden");
        }

        reorder();

    }

    ordersaver = document.getElementById("ordersaver");
    ordersaver.addEventListener("click",()=>saveNewOrder())
    function saveNewOrder(){
        tf = [...document.getElementsByClassName("tfield")]

    }

}
