M.AutoInit();

function createBar() {
    var num = parseInt(Math.random()*101,10);
    var barwrapper = document.createElement('div');
    barwrapper.className='progress';
    var bar = document.createElement('div');
    bar.className='determinate';
    bar.style="width: "+num+"%";
    barwrapper.appendChild(bar);
    document.getElementById("qq").appendChild(barwrapper);
}