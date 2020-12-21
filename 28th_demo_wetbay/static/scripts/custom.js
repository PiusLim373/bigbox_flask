
var stage_arr = ['checkconsumables', 'checkwetdrymagil','sbtransfer', 'kdtransfer', 'gptransfer', 'rttransfer', 'tptransfer', 'traytransfer', 'inditransfer', 'rtretrieval']
var stage = 0
var CheckDryWetMagil_firstpress = 1

function HideOthersExcept(){
    for(var i = 0; i < stage_arr.length; i++){
        if (i != stage) {
            id = stage_arr[i];
            $('#' + id).addClass("hide");
        }
    }
}


function UpdateCheckWetDryMagilDiv(){
    $.ajax({
        method:'POST',
        url:"/CheckWetDryMagil",
        data:{
            'from':'webui'
        },
        success:function(respond){
            var tray = respond['tray'];
            var cover = respond['cover'];
            var container = respond['container'];
            var cc = respond['cc'];
            if (respond['error']){
                $('#processfeedback').removeClass("bg-info");
                $('#processfeedback').removeClass("bg-success");
                $('#processfeedback').addClass("bg-danger");
                $('#checkdrywetmagilscard').removeClass('card-header-success');
                $('#checkdrywetmagilscard').addClass('card-header-danger');
                $('#StartProcessBtn').addClass("disabled");
                $('#StartProcessBtn').removeAttr("onclick");
            }
            else{
                $('#processfeedback').removeClass("bg-info");
                $('#processfeedback').removeClass("bg-danger");
                $('#processfeedback').addClass("bg-success");
                CardHeaderSuccess("checkdrywetmagilscard");
                $('#checkdrywetmagilscard').removeClass('card-header-danger');
                // $('#checkdrywetmagilscard').addClass('card-header-success');
                $('#StartProcessBtn').removeClass("disabled");
                $('#StartProcessBtn').attr("onclick",'StartProcess()');
            }
            for(var i=0; i<6;i++){
                var check_arr = JSON.stringify([tray[i], container[i], cover[i]]);
                if (check_arr == JSON.stringify([0,0,0])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#db'+(i+1)+ ' td').text("Not loaded");
                    $('#wb'+(i+1)).removeClass("table-danger");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-warning");
                    $('#db'+(i+1)).removeClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-warning");
                }
                else if (check_arr  == JSON.stringify([0,0,1])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#db'+(i+1)+ ' td').text("Container not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).removeClass("table-warning");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).removeClass("table-warning");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([0,1,0])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#db'+(i+1)+ ' td').text("Cover not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).removeClass("table-warning");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).removeClass("table-warning");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr == JSON.stringify([0,1,1])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).removeClass("table-warning");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-warning");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([1,0,0])){
                    $('#db'+(i+1)+ ' td').text("Not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([1,0,1])){
                    $('#db'+(i+1)+ ' td').text("Container not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).removeClass("table-warning");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).removeClass("table-warning");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([1,1,0])){
                    $('#db'+(i+1)+ ' td').text("Cover not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).removeClass("table-warning");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).removeClass("table-warning");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([1,1,1])){
                    $('#db'+(i+1)+ ' td').text("OK");
                    $('#wb'+(i+1)+ ' td').text("OK");
                    $('#wb'+(i+1)).removeClass("table-warning");
                    $('#wb'+(i+1)).removeClass("table-danger");
                    $('#wb'+(i+1)).addClass("table-success");
                    $('#db'+(i+1)).removeClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-warning");
                    $('#db'+(i+1)).addClass("table-success");
                }
            }
            if (respond['magil'] < respond['pigeonhole_to_process'].length){
                $('#magil').addClass("red-text");
                $('#magil').text("Magil's Suction Tube left: " + respond['magil']);
            }
            else{
                $('#magil').removeClass("red-text");
                $('#magil').text("Magil's Suction Tube left: " + respond['magil']);
            }
            
            if(respond['pigeonhole_to_process'].length != 0){
                var string = ""
                for(var i = 0; i < respond['pigeonhole_to_process'].length; i++){
                    string += "#" + (respond['pigeonhole_to_process'][i] + 1);
                    if(i != (respond['pigeonhole_to_process'].length - 1)){
                        string += ", ";
                    }
                }
                $('#pigeonhole_to_process').text("Pigeon hole to be process: " + string);
            }
            else{
                $('#pigeonhole_to_process').text("No available Pigeon hole to process");
            }
            
        }
    });
}


function pigholecontroller(hole){
    task="extend_retract"
    $.ajax({
        method:'POST',
        url:"/pigholecontroller",
        contentType: 'application/json',
        data:JSON.stringify({
            "task":task,
            "value":hole
        }),
        success:function(respond){
            if (respond == "1"){
                // originally closed, change to extended
                $('#pig'+hole).addClass("text-white");
                $('#pig'+hole).addClass("blackbg");
                $('#pig'+hole).html("Retract Pigeonhole #" + hole);
            }
            else if(respond == "0"){
                $('#pig'+hole).removeClass("text-white");
                $('#pig'+hole).removeClass("blackbg");
                $('#pig'+hole).html("Pop out Pigeonhole #" + hole);
            }
            else{
                console.log("invalid respond");
            }
        }
    });
}

function get_wetbay_status(){
    $.ajax({
        method:'GET',
        url:"/get_status",
        success:function(respond){
            var pigeonhole_status = [0,0,0,0,0,0];
            for (var i = 0; i <6; i++){
                pigeonhole_status[i] = parseInt(respond.split(",")[i]);
                if (pigeonhole_status[i] == 1){
                    $('#pig'+(i+1)+"status").html("pigeonhole #" +(i+1)+"<br/>ready");
                    $('#pig'+(i+1)+"status").removeClass("btn-warning");
                    $('#pig'+(i+1)+"status").addClass("btn-success");
                }
                else{
                    $('#pig'+(i+1)+"status").html("pigeonhole #" +(i+1)+"<br/>tray not loaded");
                    $('#pig'+(i+1)+"status").removeClass("btn-success");
                    $('#pig'+(i+1)+"status").addClass("btn-warning");
                }
            }
            // console.log(pigeonhole_status);
            
            // if (respond == "1"){
            //     // originally closed, change to extended
            //     $('#pig'+hole).addClass("text-white");
            //     $('#pig'+hole).addClass("blackbg");
            //     $('#pig'+hole).html("Retract Pigeonhole #" + hole);
            // }
            // else if(respond == "0"){
            //     $('#pig'+hole).removeClass("text-white");
            //     $('#pig'+hole).removeClass("blackbg");
            //     $('#pig'+hole).html("Pop out Pigeonhole #" + hole);
            // }
            // else{
            //     console.log("invalid respond");
            // }
        }
    });
}