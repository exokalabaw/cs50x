window.onload = () => {
    const title = document.getElementById("title");
    const desc = document.getElementById("desc");
    const qs = document.getElementById("quizsaver");
    const public = document.getElementById("public");
    public.addEventListener("change", checkInput);
    title.addEventListener("input", checkInput);
    desc.addEventListener("input", checkInput);

    function checkInput(){
        let oneisempty = false;
        if(title.value.length < 1||desc.value.length<1){
            oneisempty = true;
        }
        if(oneisempty){
            qs.disabled = true;
        }else{
            qs.disabled = false;
        }

    }
}
