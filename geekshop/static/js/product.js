
function first(id_suffix) {
  document.getElementById("second_hide_" + id_suffix).setAttribute("style", "opacity:1; transition: 5s; height: 100%;");
  document.getElementById("first_" + id_suffix).setAttribute("style", "display: block; transition: 5s; animation: zoomIn;");
  document.getElementById("first_yelloy_" + id_suffix).setAttribute("style", "display: block; transition: 5s; animation: zoomIn;");
}

function first_yelloy(id_suffix) {
  document.getElementById("second_hide_" + id_suffix).setAttribute("style", "opacity:0; display: none; transition: 5s;");
  document.getElementById("first_yelloy_" + id_suffix).setAttribute("style", "display: none; transition: 5s;");
  document.getElementById("first_" + id_suffix).setAttribute("style", "display: block; transition: 5s;");
}

function viewDiv() {
  document.getElementById('links').style = 'width: 230px; transition: .4s;';
  document.getElementById('nav-link').style = 'opacity: 1; transform: translateX(0px); transition: 2.3s;';
  document.getElementById('inpt').style = 'border-top-right-radius: 0; border-bottom-right-radius: 0; transition: 0.2s;';

  document.getElementById('link-1').style = 'opacity: 1; transform: translateX(20px); transition: 0.3s;';
  document.getElementById('link-2').style = 'opacity: 1; transform: translateX(20px); transition: 0.6s;';
  document.getElementById('link-3').style = 'opacity: 1; transform: translateX(20px); transition: 0.9s;';
}

function hidDiv() {
  document.getElementById('links').style = 'width: 60px; transition: .6s;';
  document.getElementById('nav-link').style = 'opacity: 0; transform: translateX(0px);  transition: 0.3s;';
  document.getElementById('inpt').style = 'border-top-right-radius: 100%; border-bottom-right-radius: 100%; transition: 0.5s;';

  document.getElementById('link-1').style = 'opacity: 0; transform: translateX(-20px); transition: 0.8s;';
  document.getElementById('link-2').style = 'opacity: 0; transform: translateX(-20px); transition: 0.5s;';
  document.getElementById('link-3').style = 'opacity: 0; transform: translateX(-20px); transition: 0.2s;';
};


