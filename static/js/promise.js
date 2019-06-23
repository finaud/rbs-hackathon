M.AutoInit();

function createBar() {
    var num = parseInt(Math.random()*101,10);
    if(num%4===0){num=100;}
    var barwrapper = document.createElement('div');
    barwrapper.className='progress col m10 bar';
    var bar = document.createElement('div');
    bar.className='determinate';
    bar.style="width: "+num+"%";
    barwrapper.appendChild(bar);
    var icondiv = document.createElement("div");
    icondiv.className="col m2";
    icondiv.style="text-align: center";
    var icon = document.createElement('i');
    icon.className="material-icons";
    if(num===100){icon.innerText="check";}
    else {icon.innerText="access_time";}
    icondiv.appendChild(icon);
    document.getElementById('qq').appendChild(icondiv);
        document.getElementById("qq").appendChild(barwrapper);

}