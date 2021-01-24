
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Global variables
// --- Div that we hide-behind and pop-up-on-top of the main web page, eg. to say "please wait while container is being launched"
var div_to_hide = ["waiting_div"];
// --- Action specification, when showing the waiting div
var action_specification = "";




// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Loading functions
window.onload = function()
{
  // --- It's important that "index.html" is not in the url!!!
  href_url = window.location.href.split("/");
  href_url = href_url[href_url.length-1];
  if (href_url.trim() == "index.html")
  {
    href_url = window.location.href.split("index.html")[0];
    window.location.href = href_url;
  }

  // --- This checks for the terminal log-file to give a live-update to the user
  setInterval(function(){get_terminal_output();}, 1000);

  // --- This is the main tab we open when launching the app
  last_tab = getCookie('last_selected_tab');
  if (last_tab == "")
  {
    document.getElementById("TAB_Set-up").click();
  }else
  {
    document.getElementById(last_tab).click();
  }

  // --- Nice sizing of container and result logs
  current_tab = getCookie('last_selected_tab');
  current_tab = current_tab.split("TAB_")[1];
  current_tab = document.getElementById(current_tab);
  box_width  = current_tab.clientWidth;
  box_height = $(window).height();
  document.getElementById("run_comments"   ).style.height = 0.60*box_height + "px";
  document.getElementById("run_comments"   ).style.width  = 0.95*box_width  + "px";
  document.getElementById("result_comments").style.height = 0.60*box_height + "px";

  // --- Hide all utility div's
  for (i = 0; i < div_to_hide.length; ++i)
  {
    document.getElementById(div_to_hide[i]).style.visibility="hidden";
    document.getElementById(div_to_hide[i]).style.zIndex=-1000;
    document.getElementById(div_to_hide[i]).style.height=0;
    document.getElementById(div_to_hide[i]).style.overflow="hidden";
  }

  // --- Make sure the vvuq drop-down is on the correct option
  selected_vvuq = getCookie('selected_vvuq');
  set_vvuq_selector(selected_vvuq);

  // --- Make sure the image drop-down is on the correct option
  reload_image_selector();
  selected_image = getCookie('selected_image');
  set_image_selector(selected_image);

  // --- Make sure the cloud drop-down is on the correct option
  selected_cloud = getCookie('selected_cloud');
  set_cloud_selector(selected_cloud);
  selected_cpu = getCookie('selected_cpu');
  set_cpu_selector(selected_cpu);
  selected_RAM = getCookie('selected_RAM');
  set_RAM_selector(selected_RAM);

  // --- Make sure the run drop-down is on the correct option
  reload_run_selector();
  selected_run = getCookie('selected_run');
  set_run_selector(selected_run);

  // --- Make sure the file drop-down is on the correct option
  reload_file_selector();
  selected_file = getCookie('selected_file');
  file_select_change(selected_file);

  // --- Make sure the data-file drop-down is on the correct option
  reload_data_file_selector();
  selected_data_file = getCookie('selected_data_file');
  data_file_select_change(selected_data_file);

  // --- Make sure the file drop-down is on the correct option
  reload_result_selector();
  selected_result = getCookie('selected_result');
  result_select_change(selected_result);

  // --- Empty terminal output
  empty_terminal_output();

}









// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Interactive waiting div : show/hide functions
function show_waiting_div()
{
  document.getElementById("waiting_div").style.position="absolute";
  document.getElementById("waiting_div").style.marginLeft="5%";
  document.getElementById("waiting_div").style.width="90%";
  document.getElementById("waiting_div").style.top="5%";
  document.getElementById("waiting_div").style.height="80%";
  document.getElementById("waiting_div").style.zIndex=3000;
  document.getElementById("waiting_div").style.visibility="visible";
  document.getElementById("waiting_gif").style.visibility="hidden";
  document.getElementById("action_wrapper_button").style.visibility="visible";
  document.getElementById("button_hide_waiting_div_upload").style.visibility="visible";
}
function show_waiting_div_with_message(message)
{
  show_waiting_div();
  document.getElementById("waiting_gif").style.visibility="visible";
  document.getElementById("action_wrapper_button").style.visibility="hidden";
  document.getElementById("button_hide_waiting_div_upload").style.visibility="visible";
  document.getElementById("waiting_message").innerHTML="<br/>"+message+"<br/>";
}
function hide_waiting_div()
{
  document.getElementById("action_wrapper_button").style.visibility="hidden";
  document.getElementById("button_hide_waiting_div_upload").style.visibility="hidden";
  document.getElementById("waiting_div").style.visibility="hidden";
  document.getElementById("waiting_gif").style.visibility="hidden";
  document.getElementById("waiting_div").style.zIndex=-3000;
  empty_terminal_output();
}




// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Open/Close Tabs for actions
function openTab(evt, selected_tab)
{
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(selected_tab).style.display = "block";
  evt.currentTarget.className += " active";

  // --- Set Cookie for next reload
  setCookie('last_selected_tab','TAB_'+selected_tab,7);
}



// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Generic function that sends php requests server-side to execute command lines
// --- The function takes a linux command, and prints its output to the innerHTML of the div named by output_destination
function execute_command_async(command,output_destination)
{
  if (command.length == 0)
  {
    document.getElementById(output_destination).innerHTML = "";
    return;
  }else
  {
    // ===%%%=== is used as a replacement for spaces (which are not allowed in http request url...)
    command = command.replace(' ','===%%%===');
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function()
    {
      if (this.readyState == 4 && this.status == 200)
      {
        document.getElementById(output_destination).innerHTML = this.responseText;
      }
    };
    xmlhttp.open("GET", "../php/server_side_functions.php?input=" + command, true);
    xmlhttp.send();
  }
}
function execute_command(command)
{
  if (command.length == 0)
  {
    return "";
  }else
  {
    // ===%%%=== is used as a replacement for spaces (which are not allowed in http request url...)
    command = command.replace(' ','===%%%===');
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", "../php/server_side_functions.php?input=" + command, false);
    xmlhttp.send();
    return xmlhttp.responseText;
  }
}
function execute_command_from_html(command, output_destination)
{
  if (command.length == 0)
  {
    document.getElementById(output_destination).innerHTML = "";
    return;
  }else
  {
    output = execute_command(command);
    output = output.replace('===%%%===','<br/>');
    document.getElementById(output_destination).innerHTML = output;
    return;
  }
}
function get_terminal_output()
{
  output = execute_command('cat /VVebUQ_runs/'+who_am_i().trim()+'/terminal_command.txt ; echo ""; tail /VVebUQ_runs/'+who_am_i().trim()+'/terminal_output.txt');
  output = '<pre style="white-space: pre-wrap; white-space: -moz-pre-wrap; white-space: -pre-wrap; white-space: -o-pre-wrap; word-wrap:break-word;">'+output+'</pre>';
  document.getElementById('terminal_output').innerHTML = output;
}
function empty_terminal_output()
{
  execute_command('printf "" > /VVebUQ_runs/'+who_am_i().trim()+'/terminal_output.txt');
  execute_command('printf "" > /VVebUQ_runs/'+who_am_i().trim()+'/terminal_command.txt');
}
function who_am_i()
{
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/who_am_i.php", false);
  xmlhttp.send();
  name = xmlhttp.responseText;
  return name.trim();
}





// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Action wrapper which will be launched by the waiting-div action button and depends on the global variable "action_specification" to be set before call
function action_wrapper()
{
  // --- Hide the action button, in case of impatient users....
  document.getElementById("action_wrapper_button").style.visibility="hidden";
  // --- This should never happen...
  if (action_specification == "")
  {
    hide_waiting_div();
    return;
  }

  // --- Launch VVUQ container
  if (action_specification == "launch_vvuq")
  {
    // --- Which VVUQ software are we using?
    selected_vvuq = document.getElementById('vvuq_selector').value;
    if (selected_vvuq == 'dakota')
    {
      image_name = 'dakota_image'; //'spamela2/dakota_container:latest';
      container_name = 'dakota_container_'+who_am_i();
    }else
    {
      image_name = 'easyvvuq_image';
      container_name = 'easyvvuq_container_'+who_am_i();
    }
    document.getElementById("waiting_gif").style.visibility="visible";
    document.getElementById("waiting_message").innerHTML="<br/>Please wait while the "+selected_vvuq+" Docker image is retrieved and launched.<br/>This may take a minute or so...<br/>";
    // --- Send form
    var formdata = new FormData();
    formdata.append("VVebUQ_session_name", who_am_i().trim());
    formdata.append("docker_image", image_name);
    formdata.append("container_name", container_name);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "../php/launch_vvuq.php",true);
    // --- We do this async because we want to catch the terminal output while the request runs...
    xmlhttp.onreadystatechange = function ()
    {
      if(this.readyState == 4 && this.status == 200)
      {
        empty_terminal_output();
        hide_waiting_div();
        cloud_select_change(document.getElementById("cloud_selector").value);
        return;
      }
    };
    xmlhttp.send(formdata);
  }

  // --- Request new Prominence Token
  if (action_specification == "request_prominence_token")
  {
    // --- Which VVUQ software are we using?
    selected_vvuq = document.getElementById('vvuq_selector').value;
    if (selected_vvuq == 'dakota')
    {
      container_name = 'dakota_container_'+who_am_i().trim();
    }else
    {
      container_name = 'easyvvuq_container_'+who_am_i().trim();
    }
    // --- Some info, including the Prominence URL
    prominence_url = execute_command('docker exec '+container_name+' bash -c \'echo $PROMINENCE_OIDC_URL\'');
    document.getElementById("waiting_gif").style.visibility="visible";
    document.getElementById("waiting_message").innerHTML='<br/>Please copy the token provided by Prominence<br/>and follow this link:<br/><a href="'+prominence_url+'/device" target="_blank">'+prominence_url+'/device</a><br/>';
    // --- Send form
    var formdata = new FormData();
    formdata.append("VVebUQ_session_name", who_am_i().trim());
    formdata.append("selected_vvuq", selected_vvuq);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "../php/request_prominence_token.php",true);
    // --- We do this async because we want to catch the terminal output while the request runs...
    xmlhttp.onreadystatechange = function ()
    {
      if(this.readyState == 4 && this.status == 200)
      {
        empty_terminal_output();
        hide_waiting_div();
	location.reload();
        return;
      }
    };
    xmlhttp.send(formdata);
  }

  // --- Pull Code Docker image
  if (action_specification == "pull_code")
  { 
    Docker_image = document.getElementById("docker_image").value;
    document.getElementById("waiting_message").innerHTML="<br/>Please wait while your code image is retrieved and launched.<br/>This may take a moment depending on the image size...<br/>";
    document.getElementById("waiting_gif").style.visibility="visible";
    // --- Send form
    var formdata = new FormData();
    formdata.append("docker_image", Docker_image);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "../php/pull_image.php",true);
    // --- We do this async because we want to catch the terminal output while the request runs...
    xmlhttp.onreadystatechange = function ()
    {
      if(this.readyState == 4 && this.status == 200)
      {
        // --- Add image to registry
        Docker_image = document.getElementById("docker_image").value;
        command = 'docker images --format="{{.Repository}}:{{.Tag}},{{.ID}}" | grep '+Docker_image;
        full_name_and_id= execute_command(command);
        full_name_and_id=full_name_and_id.replace('\n','');
        full_name = full_name_and_id.split(',');
        full_name = full_name[0];
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.open("GET", "../php/image_registry.php?action=add_image&image="+full_name_and_id+"&VVebUQ_session_name="+who_am_i().trim(), false);
        xmlhttp.send();
        // --- Make sure this image is selected in drop-down after reload
        reload_image_selector();
        set_image_selector(full_name);
        hide_waiting_div();
        empty_terminal_output();
        return;
      }
    };
    xmlhttp.send(formdata);
  }

  // --- Main function: Launch VVUQ runs
  if (action_specification == "main_run")
  {
    selected_image = document.getElementById('image_selector').value;
    document.getElementById("waiting_gif").style.visibility="visible";
    document.getElementById("waiting_message").innerHTML="<br/>Please wait while containers are launched for your jobs.<br/>This may take a moment depending on the number of runs.<br/>You may close this window, the job will continue to be prepared in the background.<br/>";
    // --- Number of CPUs and memory available for the run
    n_cpu = execute_command('nproc'); // by default, we use however many processors we have on the machine when running locally
    RAM = 1; // in GB
    selected_cloud = document.getElementById('cloud_selector').value;
    if (selected_cloud == 'use_prominence')
    {
      selected_cpu = document.getElementById('cpu_selector').value;
      if (selected_cpu == 'select_n_cpu')
      {
        n_cpu = 1;
      }else
      {
        n_cpu = selected_cpu;
      }
      selected_RAM = document.getElementById('RAM_selector').value;
      if (selected_RAM != 'select_RAM')
      {
        RAM = selected_RAM;
      }
    }
    // --- Input file format
    input_file_name = document.getElementById('file_selector').value;
    filename_split = input_file_name.split('.');
    format = filename_split[filename_split.length-1];
    // --- Data input file
    input_data_file_name = document.getElementById('data_file_selector').value;
    // --- Using Prominence?
    use_prominence = 'false';
    // --- Which VVUQ software?
    selected_vvuq = document.getElementById('vvuq_selector').value;
    if (document.getElementById('cloud_selector').value == 'use_prominence') {use_prominence = 'true';}
    // --- Send form
    var formdata = new FormData();
    formdata.append("VVebUQ_session_name", who_am_i().trim());
    formdata.append("docker_image_run", selected_image);
    formdata.append("selected_vvuq", selected_vvuq);
    formdata.append("input_file_name", input_file_name);
    formdata.append("input_file_type", format);
    formdata.append("input_data_file_name", input_data_file_name);
    formdata.append("use_prominence", use_prominence);
    formdata.append("n_cpu", n_cpu);
    formdata.append("RAM", RAM);
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "../php/create_runs.php",true);
    // --- We do this async because we want to catch the terminal output while the request runs...
    xmlhttp.onreadystatechange = function ()
    {
      if(this.readyState == 4 && this.status == 200)
      {
        // --- Print the containers logs
        selected_run = execute_command('ls /VVebUQ_runs/'+who_am_i().trim()+'/ -tr | grep workdir | tail -n 1');
        selected_run = selected_run.replace("\n","");
        reload_run_selector();
        set_run_selector(selected_run);
        reload_result_selector();
        set_result_selector("select_result");
        hide_waiting_div();
        empty_terminal_output();
        return;
      }
    };
    xmlhttp.send(formdata);
  }

  // --- Remove containers belonging to specified run
  if (action_specification == "remove_containers")
  {
    select_run = document.getElementById('run_selector').value;
    if ( (select_run != "") && (select_run != "select_run") )
    {
      document.getElementById("waiting_gif").style.visibility="visible";
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      document.getElementById("waiting_message").innerHTML="<br/>Please wait while the containers are being deleted.<br/>This may take a moment depending on the number of containers...<br/>";
      // --- Call php script
      var xmlhttp = new XMLHttpRequest();
      run_name = select_run.replace("workdir_","");
      xmlhttp.open("GET", "../php/delete_run.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, false);
      xmlhttp.send();
      set_run_selector(select_run);
      hide_waiting_div();
      return;
    }else
    {
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      document.getElementById("waiting_message").innerHTML="<br/>The selected run is not valid!<br/>";
    }
  }

  // --- Remove containers belonging to specified run and remove the run-directory where this was executed (ie. remove all run data)
  if ( (action_specification == "purge_run") || (action_specification == "purge_result") )
  {
    if (action_specification == "purge_run")
    {
      select_run = document.getElementById('run_selector').value;
    }else
    {
      select_run = document.getElementById('result_selector').value;
    }
    if ( (select_run != "") && (select_run != "select_run") && (select_run != "select_result") )
    {
      document.getElementById("waiting_gif").style.visibility="visible";
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      document.getElementById("waiting_message").innerHTML="<br/>Please wait while the run is being deleted.<br/>This may take a moment depending on the number of containers...<br/>";
      run_name = select_run.replace("workdir_","");
      // --- First delete run containers
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("GET", "../php/delete_run.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, false);
      xmlhttp.send();
      // --- And then delete data
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("GET", "../php/delete_run_data.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, false);
      xmlhttp.send();
      reload_run_selector();
      set_run_selector("select_run");
      reload_result_selector();
      set_result_selector("select_result");
      hide_waiting_div();
      return;
    }else
    {
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      document.getElementById("waiting_message").innerHTML="<br/>The selected run is not valid!<br/>";
    }
  }

  // --- Download all the data of a run
  if (action_specification == "download_run")
  {
    // --- Get run name
    selected_result = document.getElementById('result_selector').value;
    run_name = selected_result.replace('workdir_','');
    if ( (selected_result != "") && (selected_result != "select_run") && (selected_result != "select_result") )
    {
      show_waiting_div_with_message("Please wait while the data is being prepared and downloaded.<br/>This may take a moment depending on the size of the job...");
      // --- Call php script
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("GET", "../php/download_run.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name+"&get_back_to_js=true", true);
      // --- We do this async because we want to catch the terminal output while the request runs...
      xmlhttp.onreadystatechange = function ()
      {
        if(this.readyState == 4 && this.status == 200)
        {
	  hide_waiting_div();
          empty_terminal_output();
          // --- Create artificial link to download target
          link = document.createElement("a");
          link.download = run_name+'.zip';
          link.href = '../VVebUQ_downloads/'+who_am_i().trim()+'/'+run_name+'.zip';
          link.click();
          return;
        }
      };
      xmlhttp.send();
    }else
    {
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      document.getElementById("waiting_message").innerHTML="<br/>The selected run is not valid!<br/>";
      return;
    }
  }

  // --- Download all the data of a run
  if (action_specification == "get_download_urls")
  {
    selected_result = document.getElementById('result_selector').value;
    if ( (selected_result != "") && (selected_result != "select_run") && (selected_result != "select_result") )
    {
      // --- When using Prominence, this cannot be done yet (because result is in ECHO as a tarball)
      use_prominence = false;
      prominence_id = execute_command('cat /VVebUQ_runs/'+who_am_i().trim()+'/'+selected_result+'/prominence_workflow_id.txt');
      prominence_id = prominence_id.trim();
      if ( (! prominence_id.includes('No such file or directory')) && (prominence_id != '') ) {use_prominence = true;}
      if (! use_prominence)
      {
        document.getElementById("waiting_message").innerHTML = "Getting download-URLs is reserved to Prominence runs.<br/>"
                                                             + "If you are running locally, this is not necessary since files are local.";
        document.getElementById("action_wrapper_button").style.visibility="hidden";
        return;
      }
      // --- Create artificial link to download target
      show_waiting_div_with_message("Please wait while the data is being prepared and downloaded.<br/>This may take a moment depending on the size of the job...");
      // --- Get run name
      run_name = selected_result.replace('workdir_','');
      // --- Call php script
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("GET", "../php/get_download_urls.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name+"&get_back_to_js=true", true);
      // --- We do this async because we want to catch the terminal output while the request runs...
      xmlhttp.onreadystatechange = function ()
      {
        if(this.readyState == 4 && this.status == 200)
        {
          hide_waiting_div();
          empty_terminal_output();
          // --- Create artificial link to download target
          link = document.createElement("a");
          link.download = run_name+'.zip';
          link.href = '../VVebUQ_downloads/'+who_am_i().trim()+'/'+run_name+'.zip';
          link.click();
          return;
        }
      };
      xmlhttp.send();
    }else
    {
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      document.getElementById("waiting_message").innerHTML="<br/>The selected run is not valid!<br/>";
      return;
    }
  }

}






// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Launch VVUQ container
function launch_vvuq_container()
{
  // --- First check that there isn't a VVUQ container already running
  selected_vvuq = document.getElementById('vvuq_selector').value;
  container_running = check_vvuq_container();
  if (container_running.includes(selected_vvuq))
  {
    document.getElementById("vvuq_comments").innerHTML=selected_vvuq+" container already running!";
  }else
  // --- Launch a new container
  {
    show_waiting_div();
    document.getElementById("waiting_message").innerHTML="<br/>This will launch a "+selected_vvuq+" Docker container in the background.<br/>Are you sure you want to action this request?<br/>";
    action_specification = "launch_vvuq";
  }
}
function check_vvuq_container()
{
  container_running = "";
  dakota_id = execute_command("docker ps -aqf name=dakota_container_"+who_am_i()+" --filter status=running");
  dakota_id = dakota_id.replace('\n','');
  easyvvuq_id = execute_command("docker ps -aqf name=easyvvuq_container_"+who_am_i()+" --filter status=running");
  easyvvuq_id = easyvvuq_id.replace('\n','');
  if ( (dakota_id != "") && (easyvvuq_id != "") )
  {
    container_running = "dakota_and_easyvvuq";
  }
  if ( (dakota_id != "") && (easyvvuq_id == "") )
  {
    container_running = "dakota";
  }
  if ( (dakota_id == "") && (easyvvuq_id != "") )
  {
    container_running = "easyvvuq";
  }
  return container_running;
}






// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- VVUQ selection functions
function vvuq_select(selected_option)
{ 
  setCookie('selected_vvuq',selected_option.value,7);
}
function set_vvuq_selector(selected_vvuq)
{
  if (selected_vvuq == '')
  {
    vvuq_select_change('dakota');
    return;
  }else
  {
    vvuq_select_change(selected_vvuq);
    return;
  }
}
function vvuq_select_change(optionValToSelect)
{
  selectElement = document.getElementById('vvuq_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      vvuq_select(selectElement);
      break;
    }
  }
}





// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Code container functions
function pull_code_image()
{
  // --- Check if image has already been built
  Docker_image   = document.getElementById("docker_image").value;
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/image_registry.php?action=check_image&image="+Docker_image+"&VVebUQ_session_name="+who_am_i().trim(), false);
  xmlhttp.send();
  image_found = xmlhttp.responseText;
  // --- Just check image exists if not running locally
  local_runs = execute_command('cat config.in | grep -i LOCAL_RUNS_ALLOWED').split(' = ')[1].trim();
  if (! local_runs.toLowerCase().includes('true'))
  {
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", "../php/check_image.php?docker_image="+Docker_image, false);
    xmlhttp.send();
    image_exists = xmlhttp.responseText;
    if (image_exists.trim() != '')
    {
      full_name_and_id= Docker_image.trim()+',nonlocal';
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.open("GET", "../php/image_registry.php?action=add_image&image="+full_name_and_id+"&VVebUQ_session_name="+who_am_i().trim(), false);
      xmlhttp.send();
      // --- Make sure this image is selected in drop-down after reload
      reload_image_selector();
      set_image_selector(Docker_image);
      return;
    }else
    {
      show_waiting_div();
      document.getElementById("waiting_message").innerHTML="<br/>The image you specified cannot be found on the Docker hub registry."
                                                          +"<br/>Please double check or contact VVebUQ developers.<br/>";
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      return;
    }
  }
  // --- If running locally, pull image
  show_waiting_div();
  if (image_found == "found")
  { 
    document.getElementById("waiting_message").innerHTML="<br/>WARNING: you already have a built image for:"
                                                        +"<br/>"+Docker_image+"<br/>"
                                                        +"<br/>This will over-write it with a new (updated?) image."
                                                        +"<br/>Are you sure you want to action this request?<br/>";
  }else
  {
    document.getElementById("waiting_message").innerHTML="<br/>This will pull a new Docker image of your code."
		                                        +"<br/>Are you sure you want to action this request?<br/>";
  }
  action_specification = "pull_code";
}
function get_code_images()
{
  // --- Sanity check for the registered images
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/image_registry.php?action=get_all_images&image=not_needed"+"&VVebUQ_session_name="+who_am_i().trim(), false);
  xmlhttp.send();
  all_images = xmlhttp.responseText;
  output = [];
  if (all_images != "")
  { 
    all_images = all_images.split("___%%%___");
    for (i=0; i < all_images.length; ++i)
    { 
      if (all_images[i] != "")
      {
        split_name_id = all_images[i].split("%%%___%%%"); 
        output.push(split_name_id[0]);
      }
    }
  }
  return output;
}
function get_code_image_id(image_name)
{
  // --- Sanity check for the registered images
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/image_registry.php?action=get_all_images&image=not_needed"+"&VVebUQ_session_name="+who_am_i().trim(), false);
  xmlhttp.send();
  all_images = xmlhttp.responseText;
  if (all_images != "")
  {
    all_images = all_images.split("___%%%___");
    for (i=0; i < all_images.length; ++i)
    {
      if (all_images[i] != "")
      { 
        split_name_id = all_images[i].split("%%%___%%%");
        if (split_name_id[0] == image_name)
        {
          return split_name_id[1];
        }
      }
    }
  }
  return "";
}   
function image_select(selected_option)
{
  document.getElementById("new_image_form").style.visibility="hidden";
  document.getElementById("image_comments").innerHTML="";
  if (selected_option.value == "new_image")
  {
    document.getElementById("new_image_form").style.visibility="visible";
    setCookie('selected_image','new_image',7);
  }else
  {
    if (selected_option.value != "select_image")
    {
      document.getElementById("image_comments").innerHTML="Selected image:<br/>"+selected_option.value;
      setCookie('selected_image',selected_option.value,7);
    }else
    {
      setCookie('selected_image','select_image',7);
    }
  }
}
function image_select_change(optionValToSelect)
{
  selectElement = document.getElementById('image_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      image_select(selectElement);
      break;
    }
  }
}
function reload_image_selector()
{
  // --- Sanity check for the registered images
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/image_registry.php?action=sanity_check&image=not_needed"+"&VVebUQ_session_name="+who_am_i().trim(), false);
  xmlhttp.send();

  // --- Clean up selector
  selector = document.getElementById("image_selector");
  child = selector.lastElementChild;  
  while (child)
  {
    selector.removeChild(child); 
    child = selector.lastElementChild; 
  }

  // --- Re-add the basic messages
  new_image = document.createElement('option');
  new_image.setAttribute("value","select_image");
  new_image.innerHTML = "Select image";
  selector.appendChild(new_image);
  new_image = document.createElement('option');
  new_image.setAttribute("value","new_image");
  new_image.innerHTML = "New image";
  selector.appendChild(new_image);

  // --- Check if we have Code docker images available and add them to selector
  code_images = get_code_images();
  for (i=0 ; i<code_images.length ; ++i)
  {
    new_image = document.createElement('option');
    new_image.setAttribute("value",code_images[i]);
    new_image.innerHTML = code_images[i];
    selector.appendChild(new_image);
  }
}
function set_image_selector(selected_image)
{
  // --- That's the simple cases
  if (selected_image == '')
  {
    image_select_change('select_image');
    return;
  }
  if ( (selected_image == 'new_image') || (selected_image == 'select_image') )
  { 
    image_select_change(selected_image);
    return;
  }
  // --- Otherwise make sure the cookie image still exists in the registry before selecting it
  code_images = get_code_images();
  found_image = 'false';
  for (i=0 ; i<code_images.length ; ++i)
  { 
    if (code_images[i] == selected_image)
    { 
      image_select_change(selected_image);
      found_image ='true';
      break;
    }
  }
  if (found_image == 'false')
  { 
    image_select_change('select_image');
  }
}
function download_user_example()
{
  execute_command('cd ../ ; zip -r example_user_workflow.zip ./example_user_workflow ; cd -');
  link = document.createElement("a");
  link.download = "download_docker_example.zip";
  link.href = "../example_user_workflow.zip";
  link.click();
}






// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Cloud selection functions
function cloud_select(selected_option)
{ 
  document.getElementById("prominence_token_button").style.visibility="hidden";
  document.getElementById("cpu_selector").style.visibility="hidden";
  document.getElementById("RAM_selector").style.visibility="hidden";
  document.getElementById("cloud_comments").innerHTML="";
  if (selected_option.value == "use_prominence")
  {
    // --- First check the VVUQ container is running
    selected_vvuq = document.getElementById('vvuq_selector').value;
    container_running = check_vvuq_container();
    local_runs = execute_command('cat config.in | grep -i LOCAL_RUNS_ALLOWED').split(' = ')[1].trim();
    if (  (! container_running.includes(selected_vvuq)) && (local_runs.toLowerCase().includes('true'))   )
    {
      show_waiting_div();
      document.getElementById("waiting_message").innerHTML="<br/>You have not launched the VVUQ software needed to run! (go to \"Set-up\" Tab)<br/>";
      document.getElementById("action_wrapper_button").style.visibility="hidden";
      cloud_select_change('run_locally');
      return;
    }
    // --- Check if Prominence Token already exists
    existing_token = check_for_existing_token();
    if (existing_token == '')
    {
      document.getElementById("cloud_comments").innerHTML="No Prominence Token Found, request new one!";
    }else
    {
      document.getElementById("cloud_comments").innerHTML="Current Prominence Token still valid,<br/>no need for new token,<br/>proceed to following step...";
    }
    document.getElementById("prominence_token_button").style.visibility="visible";
    document.getElementById("cpu_selector").style.visibility="visible";
    document.getElementById("RAM_selector").style.visibility="visible";
    setCookie('selected_cloud','use_prominence',7);
  }else
  { 
    document.getElementById("cpu_selector").style.visibility="visible";
    setCookie('selected_cloud','run_locally',7);
  }
}
function set_cloud_selector(selected_cloud)
{
  // --- First check if local runs are allowed
  local_runs = execute_command('cat config.in | grep -i LOCAL_RUNS_ALLOWED').split(' = ')[1].trim();
  // --- If local runs are not allowed, we remove it from the selector
  if (! local_runs.toLowerCase().includes('true'))
  {
    // --- Remove local-run option
    selector = document.getElementById("cloud_selector");
    children = selector.children;
    for (i = 0; i < children.length; i++)
    {
      child = children[i];
      if (child.value == 'run_locally')
      {
        selector.removeChild(child);
      }
    }
    child = selector.lastElementChild;
    cloud_select_change(child.value);
  }else
  {
    // --- That's the simple cases
    if (selected_cloud == '')
    {
      cloud_select_change('run_locally');
      return;
    }else
    { 
      cloud_select_change(selected_cloud);
      return;
    }
  }
}
function cloud_select_change(optionValToSelect)
{
  selectElement = document.getElementById('cloud_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      cloud_select(selectElement);
      break;
    }
  }
}
function check_for_existing_token()
{
  // --- Which VVUQ software are we using?
  selected_vvuq = document.getElementById('vvuq_selector').value;
  container_running = check_vvuq_container();
  if (! container_running.includes(selected_vvuq))
  {
    return '';
  }
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  command = 'docker exec '+selected_vvuq+'_container_'+who_am_i()+' bash -c \'cat $HOME/.prominence/token\'';
  prominence_token = execute_command(command);
  prominence_token = prominence_token.split('{"access_token": "');
  if (prominence_token.length == 2)
  {
    prominence_token = prominence_token[1].split('"')[0];
    command = 'docker exec -t '+selected_vvuq+'_container_'+who_am_i()+' bash -c \'curl -i -H "Authorization: Bearer '+prominence_token+'" $PROMINENCE_OIDC_URL/userinfo\'';
    token_valid = execute_command(command);
    token_valid = token_valid.split('200 OK');
    hide_waiting_div();
    if (token_valid.length == 2)
    {
      return 'yes';
    }else
    {
      return '';
    }
  }else
  {
    hide_waiting_div();
    return '';
  }
}
function check_for_existing_token_background()
{
  // --- Which VVUQ software are we using?
  selected_vvuq = document.getElementById('vvuq_selector').value;
  container_running = check_vvuq_container();
  if (! container_running.includes(selected_vvuq))
  {
    print_expired_prominence_token_warning();
    return;
  }
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  command = 'docker exec '+selected_vvuq+'_container_'+who_am_i()+' bash -c \'cat $HOME/.prominence/token\'';
  // ===%%%=== is used as a replacement for spaces (which are not allowed in http request url...)
  command = command.replace(' ','===%%%===');
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/server_side_functions.php?input=" + command, true);
  // --- We do this async because we want to catch the terminal output while the request runs...
  xmlhttp.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      prominence_token = xmlhttp.responseText;
      prominence_token = prominence_token.split('{"access_token": "');
      if (prominence_token.length == 2)
      {
        prominence_token = prominence_token[1].split('"')[0];
        command = 'docker exec -t '+selected_vvuq+'_container_'+who_am_i()+' bash -c \'curl -i -H "Authorization: Bearer '+prominence_token+'" $PROMINENCE_OIDC_URL/userinfo\'';
        // ===%%%=== is used as a replacement for spaces (which are not allowed in http request url...)
        command = command.replace(' ','===%%%===');
        var xmlhttp2 = new XMLHttpRequest();
        xmlhttp2.open("GET", "../php/server_side_functions.php?input=" + command, true);
        // --- We do this async because we want to catch the terminal output while the request runs...
        xmlhttp2.onreadystatechange = function ()
        {
          if(this.readyState == 4 && this.status == 200)
          {
            token_valid = xmlhttp2.responseText;
            token_valid = token_valid.split('200 OK');
            if (token_valid.length == 2)
            {
              hide_waiting_div();
              return;
            }else
            {
              print_expired_prominence_token_warning();
              return;
	    }
          }
	};
	xmlhttp2.send();
      }else
      {
        print_expired_prominence_token_warning();
        return;
      }
    }
  };
  xmlhttp.send();
}
function expired_prominence_token_warning()
{
  selected_cloud = document.getElementById('cloud_selector').value;
  if (selected_cloud != 'use_prominence') {return "n/a";}
  existing_token = check_for_existing_token();
  if (existing_token == '')
  {
    print_expired_prominence_token_warning();
    return "expired";
  }
}
function print_expired_prominence_token_warning()
{
    show_waiting_div();
    document.getElementById("waiting_message").innerHTML="<br/>Your Prominence Token has expired! (go to \"Cloud\" Tab)<br/>";
    document.getElementById("cloud_comments").innerHTML="No Prominence Token Found, request new one!";
    document.getElementById("action_wrapper_button").style.visibility="hidden";
    document.getElementById("button_hide_waiting_div_upload").style.visibility="visible";
    document.getElementById("waiting_gif").style.visibility="hidden";
    return;
}
function request_prominence_token()
{
  // --- First check the VVUQ container is running
  selected_vvuq = document.getElementById('vvuq_selector').value;
  container_running = check_vvuq_container();
  if (! container_running.includes(selected_vvuq))
  {
    show_waiting_div();
    document.getElementById("waiting_message").innerHTML="<br/>You have not launched the VVUQ software needed to run! (go to \"Set-up\" Tab)<br/>";
    document.getElementById("action_wrapper_button").style.visibility="hidden";
    return;
  }
  // --- Go to run
  show_waiting_div();
  document.getElementById("waiting_message").innerHTML="<br/>This will request a new Prominence Token.<br/>Are you sure you want to action this request?<br/>";
  action_specification = "request_prominence_token";
}
// --- CPU selection functions
function cpu_select(selected_option)
{ 
  // --- Check if Prominence Token already exists
  check_for_existing_token_background();
  setCookie('selected_cpu',selected_option.value,7);
}
function set_cpu_selector(selected_cpu)
{
  // --- That's the simple cases
  if (selected_cpu == '')
  {
    cpu_select_change('select_n_cpu');
    return;
  }else
  { 
    cpu_select_change(selected_cpu);
    return;
  }
}
function cpu_select_change(optionValToSelect)
{
  selectElement = document.getElementById('cpu_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      cpu_select(selectElement);
      break;
    }
  }
}
// --- RAM selection functions
function RAM_select(selected_option)
{ 
  // --- Check if Prominence Token already exists
  check_for_existing_token_background();
  setCookie('selected_RAM',selected_option.value,7);
}
function set_RAM_selector(selected_RAM)
{
  // --- That's the simple cases
  if (selected_RAM == '')
  {
    RAM_select_change('select_RAM');
    return;
  }else
  { 
    RAM_select_change(selected_RAM);
    return;
  }
}
function RAM_select_change(optionValToSelect)
{
  selectElement = document.getElementById('RAM_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      RAM_select(selectElement);
      break;
    }
  }
}







// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Main run functions
function launch_main_run()
{
  // --- First check the VVUQ container is running
  container_running = check_vvuq_container();
  if (container_running == "")
  {
    show_waiting_div();
    document.getElementById("waiting_message").innerHTML="<br/>You have not launched the VVUQ software needed to run! (go to \"Set-up\" Tab)<br/>";
    document.getElementById("action_wrapper_button").style.visibility="hidden";
    return;
  }
  // --- Check there is an input file
  input_file_present = check_input_file();
  if (input_file_present == "false")
  {
    show_waiting_div();
    document.getElementById("waiting_message").innerHTML="<br/>You have not uploaded any input file needed to run! (go to \"Inputs\" Tab)<br/>";
    document.getElementById("action_wrapper_button").style.visibility="hidden";
    return;
  }
  // --- Check an image has been selected
  selected_image = document.getElementById('image_selector').value;
  if ( (selected_image == "") || (selected_image == "select_image") || (selected_image == "new_image") )
  {
    show_waiting_div();
    document.getElementById("waiting_message").innerHTML="<br/>You have not selected any code image needed to run! (go to \"Set-up\" Tab)<br/>";
    document.getElementById("action_wrapper_button").style.visibility="hidden";
    return;
  }
  // --- Check Prominence Token is not expired (if using Prominence)
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token_before_run.php?VVebUQ_session_name="+who_am_i().trim()+"&selected_vvuq="+container_running, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Go to run
        show_waiting_div();
        document.getElementById("waiting_message").innerHTML="<br/>This will launch the VVUQ job with your code.<br/>Are you sure you want to action this request?<br/>";
        action_specification = "main_run";
      }else
      {
        print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function run_select(selected_option)
{
  document.getElementById("run_comments").innerHTML="";
  if (selected_option.value != "select_run")
  {
    // --- Get run name
    setCookie('selected_run',selected_option.value,7);
    dir_name = selected_option.value;
    run_name = dir_name.split("workdir_");
    run_name = run_name[1];
    // --- Check Prominence Token is not expired (if using Prominence)
    selected_result = document.getElementById('run_selector').value;
    run_name = selected_result.replace('workdir_','');
    show_waiting_div_with_message("Checking Prominence Token, please wait...");
    var xmlhttp_check = new XMLHttpRequest();
    xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
    xmlhttp_check.onreadystatechange = function ()
    {
      if(this.readyState == 4 && this.status == 200)
      {
        validity = xmlhttp_check.responseText;
        if (validity != "expired")
        {
          hide_waiting_div();
          // --- Call php script
          show_waiting_div_with_message("Getting run status, please wait...");
          var xmlhttp = new XMLHttpRequest();
          xmlhttp.open("GET", "../php/get_run_status.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
          xmlhttp.onreadystatechange = function ()
          {
            if(this.readyState == 4 && this.status == 200)
            {
              hide_waiting_div();
              // --- print the docker containers corresponding to job
              containers = xmlhttp.responseText;
              containers = "<pre>" + containers + "</pre>";
              document.getElementById("run_comments").innerHTML = containers;
              return;
            }
          };
          xmlhttp.send();
          return;
        }else
        {
          print_expired_prominence_token_warning();
        }
      }
    };
    xmlhttp_check.send();
  }else
  {
    setCookie('selected_run','select_run',7);
  }
}
function run_select_change(optionValToSelect)
{
  selectElement = document.getElementById('run_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      run_select(selectElement);
      break;
    }
  }
}
function get_previous_runs()
{
  previous_runs = [];
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/list_runs.php?VVebUQ_session_name="+who_am_i().trim(), false);
  xmlhttp.send();
  output = xmlhttp.responseText;
  output = output.split("\n");
  for (i=0 ; i<output.length; i++)
  {
    if (output[i] != "")
    {
      previous_runs.push('workdir_'+output[i]);
    }
  }
  return previous_runs;
}
function refresh_containers_log()
{
  // --- Refresh log
  selected_run = document.getElementById('run_selector').value;
  reload_run_selector();
  run_select_change(selected_run);
}
function stop_containers()
{
  // --- Check Prominence Token is not expired (if using Prominence)
  selected_result = document.getElementById('run_selector').value;
  run_name = selected_result.replace('workdir_','');
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Go to action wrapper
        show_waiting_div();
        document.getElementById("waiting_message").innerHTML="<br/>This will stop and remove all containers for this run.<br/>"
                                                            +"Data from completed containers will still be retrievable,<br/>"
                                                            +"but you might lose data from unfinished containers.<br/>"
                                                            +"Are you sure you want to action this request?<br/>";
        action_specification = "remove_containers";
        return;
      }else
      {
        print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function purge_run()
{
  // --- Check Prominence Token is not expired (if using Prominence)
  selected_result = document.getElementById('run_selector').value;
  run_name = selected_result.replace('workdir_','');
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Go to action wrapper
        show_waiting_div();
        document.getElementById("waiting_message").innerHTML="<br/>This will stop and remove all containers for this run,<br/>"
                                                            +"and remove all data associated with this run.<br/>"
                                                            +"Are you sure you want to action this request?<br/>";
        action_specification = "purge_run";
        return;
      }else
      {
	print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function reload_run_selector()
{
  // --- Clean up selector
  selector = document.getElementById("run_selector");
  child = selector.lastElementChild;
  while (child)
  { 
    selector.removeChild(child); 
    child = selector.lastElementChild;
  }

  // --- Re-add the basic messages
  new_run = document.createElement('option');
  new_run.setAttribute("value","select_run");
  new_run.innerHTML = "Select run";
  selector.appendChild(new_run);
  
  // --- Add the other runs available
  previous_runs = get_previous_runs();
  for (i=0 ; i<previous_runs.length ; ++i)
  {
    new_run = document.createElement('option');
    new_run.setAttribute("value",previous_runs[i]);
    clean_name = previous_runs[i].split("workdir_");
    clean_name = clean_name[1];
    new_run.innerHTML = clean_name;
    selector.appendChild(new_run);
  }
}
function set_run_selector(selected_run)
{
  // --- That's the simple cases
  if ( (selected_run == '') || (selected_run == 'select_run') )
  {
    run_select_change('select_run');
    return;
  }
  // --- Otherwise make sure run still exists before selecting it
  previous_runs = get_previous_runs();
  found_run = 'false';
  for (i=0 ; i<previous_runs.length ; ++i)
  {
    if (previous_runs[i] == selected_run)
    {
      run_select_change(selected_run);
      found_run ='true';
      break;
    }
  }
  if (found_run == 'false')
  {
    run_select_change('select_run');
  }
}









// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Upload file functions
function file_select(selected_option)
{ 
  document.getElementById("upload_form").style.visibility="hidden";
  document.getElementById("file_comments").innerHTML="";
  if (selected_option.value == "new_file")
  { 
    document.getElementById("upload_form").style.visibility="visible";
    document.getElementById("progress_status").innerHTML = "";
    document.getElementById("upload_comments").innerHTML = "";
    setCookie('selected_file','new_file',7);
  }else
  { 
    setCookie('selected_file',selected_option.value,7);
  }
}
function file_select_change(optionValToSelect)
{ 
  selectElement = document.getElementById('file_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  { 
    if (opt.value == optionValToSelect)
    { 
      selectElement.selectedIndex = j;
      file_select(selectElement);
      break;
    }
  }
}
function reload_file_selector()
{ 
  // --- Clean up selector
  selector = document.getElementById("file_selector");
  child = selector.lastElementChild;
  while (child)
  { 
    selector.removeChild(child); 
    child = selector.lastElementChild;
  }
  
  // --- Re-add the basic messages
  new_file = document.createElement('option');
  new_file.setAttribute("value","select_file");
  new_file.innerHTML = "Select file";
  selector.appendChild(new_file);
  new_file = document.createElement('option');
  new_file.setAttribute("value","new_file");
  new_file.innerHTML = "New file";
  selector.appendChild(new_file);

  // --- Add the other runs available
  existing_files = get_existing_files();
  for (i=0 ; i<existing_files.length ; ++i)
  {
    new_file = document.createElement('option');
    new_file.setAttribute("value",existing_files[i]);
    new_file.innerHTML = existing_files[i];
    selector.appendChild(new_file);
  }
}
function get_existing_files()
{ 
  existing_files = [];
  output = execute_command('ls -p /VVebUQ_runs/'+who_am_i().trim()+'/ | grep -v "/" | grep -v "README.txt" | grep -v "terminal_command.txt" | grep -v "terminal_output.txt" | grep -E ".csv|.nc"');
  output = output.split("\n");
  for (i=0 ; i<output.length; i++)
  { 
    if (output[i] != "")
    { 
      existing_files.push(output[i]);
    }
  }
  return existing_files;
}
function check_input_file()
{
  file_present = "false";
  output = execute_command('ls -p /VVebUQ_runs/'+who_am_i().trim()+'/ | grep -v "/" | grep -v "README.txt" | grep -v "terminal_command.txt" | grep -v "terminal_output.txt" | grep -E ".csv|.nc"');
  output = output.replace("\n","");
  if (output != "")
  {
    file_present = "true";
  }
  return file_present;
}
function fileChosen()
{
  // --- Make folder button visible
  document.getElementById("upload_comments").innerHTML="Please click to begin upload:";
  document.getElementById("upload_div").style.visibility="visible";
  document.getElementById("upload_button").style.visibility = "visible";
  document.getElementById("progressBar").style.visibility="visible";
}
function send_upload()
{
  document.getElementById("upload_button").style.visibility = "hidden";
  document.getElementById("upload_comments").innerHTML = "upload in progress...";

  var n_files = document.getElementById("fileToUpload").files.length;
  var formdata = new FormData();
  formdata.append("VVebUQ_session_name", who_am_i().trim());
  for (k=0;k<n_files;k++)
  {
    var file = document.getElementById("fileToUpload").files[k];
    formdata.append("fileToUpload[]", file);
  }
  var ajax = new XMLHttpRequest();
  ajax.upload.addEventListener("progress", progressHandler, false);
  ajax.addEventListener("load", completeHandler, false);
  ajax.addEventListener("error", errorHandler, false);
  ajax.addEventListener("abort", abortHandler, false);
  ajax.open("POST", "../php/upload.php");
  ajax.send(formdata);
}
function progressHandler(event)
{
  var percent = (event.loaded / event.total) * 100;
  document.getElementById("progressBar").value = Math.round(percent);
  document.getElementById("progress_status").innerHTML = "upload in progress: " + Math.round(percent) + "%";
}
function completeHandler(event)
{
  document.getElementById("progress_status").innerHTML = "";
  document.getElementById("upload_comments").innerHTML=event.target.responseText;
  document.getElementById("progressBar").value = 0;
  document.getElementById("progressBar").style.visibility="hidden";
  reload_file_selector();
  last_file = execute_command('ls -ptr /VVebUQ_runs/'+who_am_i().trim()+'/ | grep -v "/" | grep -v "terminal_command.txt" | grep -v "terminal_output.txt" | grep -E ".csv|.ncd" | tail -n 1');
  last_file = last_file.replace("\n","");
  file_select_change(last_file);
}
function errorHandler(event)
{
  document.getElementById("progress_status").innerHTML = "Upload Failed";
}
function abortHandler(event)
{
  document.getElementById("progress_status").innerHTML = "Upload Aborted";
}


















// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Upload Data file functions
function data_file_select(selected_option)
{ 
  document.getElementById("upload_data_form").style.visibility="hidden";
  document.getElementById("data_file_comments").innerHTML="";
  if (selected_option.value == "new_data_file")
  { 
    document.getElementById("upload_data_form").style.visibility="visible";
    document.getElementById("data_progress_status").innerHTML = "";
    document.getElementById("data_upload_comments").innerHTML = "";
    setCookie('selected_data_file','new_data_file',7);
  }else
  { 
    setCookie('selected_data_file',selected_option.value,7);
  }
}
function data_file_select_change(optionValToSelect)
{ 
  selectElement = document.getElementById('data_file_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  { 
    if (opt.value == optionValToSelect)
    { 
      selectElement.selectedIndex = j;
      data_file_select(selectElement);
      break;
    }
  }
}
function reload_data_file_selector()
{ 
  // --- Clean up selector
  selector = document.getElementById("data_file_selector");
  child = selector.lastElementChild;
  while (child)
  { 
    selector.removeChild(child); 
    child = selector.lastElementChild;
  }
  
  // --- Re-add the basic messages
  new_file = document.createElement('option');
  new_file.setAttribute("value","select_data_file");
  new_file.innerHTML = "Select file";
  selector.appendChild(new_file);
  new_file = document.createElement('option');
  new_file.setAttribute("value","new_data_file");
  new_file.innerHTML = "New file";
  selector.appendChild(new_file);

  // --- Add the other runs available
  existing_files = get_existing_data_files();
  for (i=0 ; i<existing_files.length ; ++i)
  {
    new_file = document.createElement('option');
    new_file.setAttribute("value",existing_files[i]);
    new_file.innerHTML = existing_files[i];
    selector.appendChild(new_file);
  }
}
function get_existing_data_files()
{ 
  existing_files = [];
  output = execute_command('ls -p /VVebUQ_runs/'+who_am_i().trim()+'/ | grep -v "/" | grep -v "README.txt" | grep -v "terminal_command.txt" | grep -v "terminal_output.txt" | grep ".zip"');
  output = output.split("\n");
  for (i=0 ; i<output.length; i++)
  { 
    if (output[i] != "")
    { 
      existing_files.push(output[i]);
    }
  }
  return existing_files;
}
function check_input_data_file()
{
  file_present = "false";
  output = execute_command('ls -p /VVebUQ_runs/'+who_am_i().trim()+'/ | grep -v "/" | grep -v "README.txt" | grep -v "terminal_command.txt" | grep -v "terminal_output.txt" | grep ".zip"');
  output = output.replace("\n","");
  if (output != "")
  {
    file_present = "true";
  }
  return file_present;
}
function dataFileChosen()
{
  // --- Make folder button visible
  document.getElementById("data_upload_comments").innerHTML="Please click to begin upload:";
  document.getElementById("data_upload_div").style.visibility="visible";
  document.getElementById("data_upload_button").style.visibility = "visible";
  document.getElementById("data_progressBar").style.visibility="visible";
}
function send_data_upload()
{
  document.getElementById("data_upload_button").style.visibility = "hidden";
  document.getElementById("data_upload_comments").innerHTML = "upload in progress...";

  var n_files = document.getElementById("dataFileToUpload").files.length;
  var formdata = new FormData();
  formdata.append("VVebUQ_session_name", who_am_i().trim());
  for (k=0;k<n_files;k++)
  {
    var file = document.getElementById("dataFileToUpload").files[k];
    formdata.append("dataFileToUpload[]", file);
  }
  var ajax = new XMLHttpRequest();
  ajax.upload.addEventListener("progress", data_progressHandler, false);
  ajax.addEventListener("load", data_completeHandler, false);
  ajax.addEventListener("error", data_errorHandler, false);
  ajax.addEventListener("abort", data_abortHandler, false);
  ajax.open("POST", "../php/upload_data_file.php");
  ajax.send(formdata);
}
function data_progressHandler(event)
{
  var percent = (event.loaded / event.total) * 100;
  document.getElementById("data_progressBar").value = Math.round(percent);
  document.getElementById("data_progress_status").innerHTML = "upload in progress: " + Math.round(percent) + "%";
}
function data_completeHandler(event)
{
  document.getElementById("data_progress_status").innerHTML = "";
  document.getElementById("data_upload_comments").innerHTML=event.target.responseText;
  document.getElementById("data_progressBar").value = 0;
  document.getElementById("data_progressBar").style.visibility="hidden";
  reload_data_file_selector();
  last_file = execute_command('ls -ptr /VVebUQ_runs/'+who_am_i().trim()+'/ | grep -v "/" | grep -v "terminal_command.txt" | grep -v "terminal_output.txt" | grep ".zip" | tail -n 1');
  last_file = last_file.replace("\n","");
  data_file_select_change(last_file);
}
function data_errorHandler(event)
{
  document.getElementById("data_progress_status").innerHTML = "Upload Failed";
}
function data_abortHandler(event)
{
  document.getElementById("data_progress_status").innerHTML = "Upload Aborted";
}

















// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Result functions
function result_select(selected_option)
{ 
  // --- Check Prominence Token is not expired (if using Prominence)
  selected_result = document.getElementById('result_selector').value;
  run_name = selected_result.replace('workdir_','');
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Get results
        document.getElementById("retrieve_files_list").innerHTML = "";
        document.getElementById("result_comments").innerHTML="";
        if (selected_option.value != "select_result")
        { 
          setCookie('selected_result',selected_option.value,7);
          // --- print the docker containers corresponding to job
          run_name = selected_option.value;
          run_name = run_name.replace("workdir_","");
          // --- Call php script
          show_waiting_div_with_message("Getting run content, please wait...");
          var xmlhttp = new XMLHttpRequest();
          xmlhttp.open("GET", "../php/list_run_files.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
          xmlhttp.onreadystatechange = function ()
          { 
            if(this.readyState == 4 && this.status == 200)
            { 
              hide_waiting_div();
              output = xmlhttp.responseText;
              output_lines = output.split("\n");
              count_runs = output_lines[0].split('This run contains ')[1];
              count_runs = count_runs.split(' sub-tasks')[0];
              fullcontent = '';
              if (output.includes("At first sight, each sub-task contains"))
              {
                fullcontent = output.split("At first sight, each sub-task contains")[1];
              }
              split_content = fullcontent.split("\n");
              new_list = document.createElement("ul");
              for (i = 0; i<split_content.length; i++)
              {
                if (split_content[i].trim() != '')
                {
                  new_file = document.createElement("li");
                  new_file.setAttribute("id",split_content[i].trim());
                  new_file.setAttribute("style","cursor: pointer;");
                  new_file.setAttribute("onclick","select_result_file(this.id);");
                  new_file.innerHTML = split_content[i].trim();
                  new_list.appendChild(new_file);
                }
              }
              comments = document.createElement("div");
              comments.innerHTML = "<p>This case contains "+count_runs+" run-directories each with content:</p><br/>";
              result_div = document.getElementById("result_comments");
              result_div.appendChild(comments);
              result_div.appendChild(new_list);
              return;
            }
          };
          xmlhttp.send();
        }else
        {
          setCookie('selected_result','select_result',7);
        }
        return;
      }else
      {
        print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function result_select_change(optionValToSelect)
{
  selectElement = document.getElementById('result_selector');
  selectOptions = selectElement.options;
  for (var opt, j = 0; opt = selectOptions[j]; j++)
  {
    if (opt.value == optionValToSelect)
    {
      selectElement.selectedIndex = j;
      result_select(selectElement);
      break;
    }
  }
}
function refresh_result_list()
{ 
  selected_result = document.getElementById('result_selector').value;
  reload_result_selector();
  result_select_change(selected_result);
}
function reload_result_selector()
{ 
  // --- Clean up selector
  selector = document.getElementById("result_selector");
  child = selector.lastElementChild;
  while (child)
  { 
    selector.removeChild(child); 
    child = selector.lastElementChild;
  }
  
  // --- Re-add the basic messages
  new_run = document.createElement('option');
  new_run.setAttribute("value","select_result");
  new_run.innerHTML = "Select run";
  selector.appendChild(new_run);
  
  // --- Add the other runs available
  previous_runs = get_previous_runs();
  for (i=0 ; i<previous_runs.length ; ++i)
  {
    new_run = document.createElement('option');
    new_run.setAttribute("value",previous_runs[i]);
    clean_name = previous_runs[i].split("workdir_");
    clean_name = clean_name[1];
    new_run.innerHTML = clean_name;
    selector.appendChild(new_run);
  }
}
function set_result_selector(selected_run)
{
  // --- That's the simple cases
  if ( (selected_run == '') || (selected_run == 'select_result') )
  {
    result_select_change('select_result');
    return;
  }
  // --- Otherwise make sure run still exists before selecting it
  previous_runs = get_previous_runs();
  found_run = 'false';
  for (i=0 ; i<previous_runs.length ; ++i)
  {
    if (previous_runs[i] == selected_run)
    {
      result_select_change(selected_run);
      found_run ='true';
      break;
    }
  }
  if (found_run == 'false')
  {
    result_select_change('select_result');
  }
}
function purge_result()
{
  // --- Check Prominence Token is not expired (if using Prominence)
  selected_result = document.getElementById('result_selector').value;
  run_name = selected_result.replace('workdir_','');
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Go to action wrapper
        show_waiting_div();
        document.getElementById("waiting_message").innerHTML="<br/>This will stop and remove all containers for this run,<br/>"
                                                            +"and remove all data associated with this run.<br/>"
                                                            +"Are you sure you want to action this request?<br/>";
        action_specification = "purge_result";
        return;
      }else
      {
        print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function select_result_file(file_id)
{
  // --- When using Prominence, this cannot be done yet (because result is in ECHO as a tarball)
  use_prominence = false;
  selected_result = document.getElementById('result_selector').value;
  prominence_id = execute_command('cat /VVebUQ_runs/'+who_am_i().trim()+'/'+selected_result+'/prominence_workflow_id.txt');
  prominence_id = prominence_id.trim();
  if ( (! prominence_id.includes('No such file or directory')) && (prominence_id != '') ) {use_prominence = true;}
  if (use_prominence)
  {
    document.getElementById("retrieve_files_list").innerHTML = "Downloading selected files with Prominence is not yet possible.<br/>"
	                                                     + "You will need to download the entire run at once.";
    return;
  }
  new_list = document.getElementById("retrieve_files_list");
  file_already_selected = 'false';
  all_files = new_list.getElementsByTagName('li');
  for (i = 0; i<all_files.length; i++)
  {
    file_tmp = all_files[i];
    name_tmp = file_tmp.id;
    name_tmp = name_tmp.split("REMOVE_FILE_");
    name_tmp = name_tmp[1];
    if (name_tmp == file_id)
    {
      file_already_selected = 'true';
    }
  }
  if (file_already_selected == 'false')
  {
    new_file = document.createElement("li");
    new_file.setAttribute("id","REMOVE_FILE_"+file_id);
    new_file.setAttribute("style","cursor: pointer;");
    new_file.setAttribute("onclick","unselect_result_file(this.id);");
    new_file.innerHTML = file_id;
    new_list.appendChild(new_file);
  }
}
function unselect_result_file(file_id)
{
  filename = file_id.split("REMOVE_FILE_");
  filename = filename[1];
  new_list = document.getElementById("retrieve_files_list");
  all_files = new_list.getElementsByTagName('li');
  for (i = 0; i<all_files.length; i++)
  {
    file_tmp = all_files[i];
    name_tmp = file_tmp.id;
    name_tmp = name_tmp.split("REMOVE_FILE_");
    name_tmp = name_tmp[1];
    if (name_tmp == filename)
    {
      new_list.removeChild(file_tmp);
    }
  }
}
function download_entire_run()
{
  // --- Check Prominence Token is not expired (if using Prominence)
  selected_result = document.getElementById('result_selector').value;
  run_name = selected_result.replace('workdir_','');
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Go to action wrapper
        show_waiting_div();
        document.getElementById("waiting_message").innerHTML="<br/>This will download the entire data associated,<br/>"
                                                            +"to this run. Depending on the size of the data,<br/>"
                                                            +"the number of runs, and your internet connection,<br/>"
                                                            +"this may take a long time.<br/>"
                                                            +"(Have you considered using \"get_download_URLs\" instead?)<br/>"
                                                            +"Are you sure you want to action this request?<br/>";
        action_specification = "download_run";
        return;
      }else
      {
        print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function get_download_urls()
{
  // --- Check Prominence Token is not expired (if using Prominence)
  selected_result = document.getElementById('result_selector').value;
  run_name = selected_result.replace('workdir_','');
  show_waiting_div_with_message("Checking Prominence Token, please wait...");
  var xmlhttp_check = new XMLHttpRequest();
  xmlhttp_check.open("GET", "../php/check_prominence_token.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name, true);
  xmlhttp_check.onreadystatechange = function ()
  {
    if(this.readyState == 4 && this.status == 200)
    {
      validity = xmlhttp_check.responseText;
      if (validity != "expired")
      {
        hide_waiting_div();
        // --- Go to action wrapper
        show_waiting_div();
        document.getElementById("waiting_message").innerHTML="<br/>This will produce a list of URLs for each instance<br/>"
                                                            +"of this run. Depending on the number of instances,<br/>"
                                                            +"this may take some time.<br/>"
                                                            +"Are you sure you want to action this request?<br/>";
        action_specification = "get_download_urls";
        return;
      }else
      {
        print_expired_prominence_token_warning();
      }
    }
  };
  xmlhttp_check.send();
}
function download_selected_files()
{
  // --- When using Prominence, this cannot be done yet (because result is in ECHO as a tarball)
  use_prominence = false;
  selected_result = document.getElementById('result_selector').value;
  prominence_id = execute_command('cat /VVebUQ_runs/'+who_am_i().trim()+'/'+selected_result+'/prominence_workflow_id.txt');
  prominence_id = prominence_id.trim();
  if ( (! prominence_id.includes('No such file or directory')) && (prominence_id != '') ) {use_prominence = true;}
  if (use_prominence)
  {
    download_entire_run();
    return;
  }
  selected_result = document.getElementById('result_selector').value;
  run_name = selected_result.replace('workdir_','');
  // --- Get list of files in format for php script
  file_list = document.getElementById("retrieve_files_list");
  all_files = file_list.getElementsByTagName('li');
  file_list_php = '';
  for (i = 0; i<all_files.length; i++)
  { 
    file_tmp = all_files[i];
    name_tmp = file_tmp.id;
    name_tmp = name_tmp.split("REMOVE_FILE_");
    full_name = name_tmp[1];
    file_list_php = file_list_php+'&files[]='+full_name;
  }
  // --- Call php script
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.open("GET", "../php/download_run_files.php?VVebUQ_session_name="+who_am_i().trim()+"&run_name="+run_name+file_list_php+"&get_back_to_js=true", false);
  xmlhttp.send();
  // --- Create artificial link to download target
  link = document.createElement("a");
  link.download = run_name+'_selected.zip';
  link.href = '../VVebUQ_downloads/'+who_am_i().trim()+'/'+run_name+'_selected.zip';
  link.click();
}











// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Cookie functions
function setCookie(cname, cvalue, exdays)
{ 
  var d = new Date();
  d.setTime(d.getTime() + (exdays*24*60*60*1000));
  var expires = "expires="+d.toUTCString();
  document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname)
{   
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++)
    { 
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1);
      if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
    }
    return "";
}














// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --------------------------------------------------------------------
// --- Debug functions

function debug()
{
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.open("GET", "../php/image_registry.php?action=remove_image&image=random/image:latest"+"&VVebUQ_session_name="+who_am_i().trim(), false);
    xmlhttp.send();
    return xmlhttp.responseText;
}

