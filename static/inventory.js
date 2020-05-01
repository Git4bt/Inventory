  var dcenter = ["amazon", "michigan", "rhino", "tahoe"] 
  dcenter.forEach(getServerCount)

  async function getServerCount(dc){
      let resp = await fetch('inventory/'+dc)
      let data = await resp.json()
      if (window.location.pathname == "/update") {
        document.getElementById(dc).innerHTML = `<input type=text value=${data.servers} placeholder=${data.servers} id=${dc.toUpperCase()}>`;
      } else {
        document.getElementById(dc).innerHTML = data.servers;
      }
    }

  async function updateServers() {
    for (dc of dcenter){
      let resp = await fetch('inventory/'+dc);
      let data = await resp.json();
      let  dcobj = document.getElementById(dc.toUpperCase());
      if (dcobj.value && dcobj.placeholder != dcobj.value){
        const headerPayload = {
          headers:{ "content-type":"text/plain"},
          method: "POST",
          body:dcobj.value
        };
        let fobj = await fetch('inventory/'+dc, headerPayload);
      }
    }
  location.replace('update');
  }