// function GetStatus(){
//     $.ajax({
// 		method:'GET',
// 		url:"/DebugPageStatus",
// 		success:function(response){
//             console.log(response['shuttle'])
//             for(var i = 0; i < 6; i++){
//                 if(response['tray'][i] == 1){
//                     $('#TrayTrue' + (i+1)).addClass("selected");
//                 }
//                 else $('#TrayFalse' + (i+1)).addClass("selected")   
//             }
//             for(var i = 0; i < 6; i++){
//                 if(response['cover'][i] == 1){
//                     $('#CoverTrue' + (i+1)).addClass("selected");
//                 }
//                 else $('#CoverFalse' + (i+1)).addClass("selected")   
//             }
//             for(var i = 0; i < 6; i++){
//                 if(response['container'][i] == 1){
//                     $('#ContainerTrue' + (i+1)).addClass("selected");
//                 }
//                 else $('#ContainerFalse' + (i+1)).addClass("selected")   
//             }
//             for(var i = 0; i < 6; i++){
//                 if(response['shuttle'][i] == 1){
//                     $('#ShuttleTrue' + (i+1)).addClass("selected");
//                 }
//                 else $('#ShuttleFalse' + (i+1)).addClass("selected")   
//             }
            
// 		}
// 	});
// }
var stage_arr = ['checkconsumables', 'checkwetdrymagil','null', 'startprocess', 'mainprocess']
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

function UpdateCheckConsumablesDiv(){
    $.ajax({
        method:'POST',
        url:"/CheckConsumables",
        data:{
            'from':'webui'
        },
        success:function(respond){
            if(respond['check_success'] == 1){
                $('#processfeedback').removeClass("bg-info");
                $('#processfeedback').removeClass("bg-danger");
                $('#processfeedback').addClass("bg-success");
                $('#checkconsumablescard').removeClass("card-header-danger");
                $('#checkconsumablescard').addClass("card-header-success");
                $('#checkconsumablesfailtext').addClass("hide");
                for (var key in respond['ConsumablesDict']){
                    $('#'+key).removeClass("table-active");
                    $('#'+key).addClass("table-success");
                }
            }
            else if(respond['check_success'] == 0){
                $('#processfeedback').removeClass("bg-info");
                $('#processfeedback').removeClass("bg-success");
                $('#processfeedback').addClass("bg-danger");
                $('#checkconsumablescard').removeClass("card-header-success");
                $('#checkconsumablescard').addClass("card-header-danger");
                $('#checkconsumablesfailtext').removeClass("hide");
                for (var key in respond['ConsumablesDict']){
                    if(respond['ConsumablesDict'][key] == 1){
                        $('#'+key).removeClass("table-active");
                        $('#'+key).removeClass("table-danger");
                        $('#'+key).addClass("table-success");
                    }
                    else if(respond['ConsumablesDict'][key] == 0){
                        $('#'+key).removeClass("table-active");
                        $('#'+key).addClass("table-danger");
                    }
                    
                }
            }
            else{
                for (var key in respond['ConsumablesDict']){
                    $('#'+key).removeClass("table-danger");
                    $('#'+key).removeClass("table-success");
                    $('#'+key).addClass("table-active");
                }
            }
        }
    });
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
                $('#checkdrywetmagilscard').removeClass('card-header-danger');
                $('#checkdrywetmagilscard').addClass('card-header-success');
                $('#StartProcessBtn').removeClass("disabled");
                $('#StartProcessBtn').attr("onclick",'StartProcess()');
            }
            for(var i=0; i<6;i++){
                var check_arr = JSON.stringify([tray[i], container[i], cover[i]]);
                if (check_arr == JSON.stringify([0,0,0])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#db'+(i+1)+ ' td').text("Not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-warning");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-warning");
                }
                else if (check_arr  == JSON.stringify([0,0,1])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#db'+(i+1)+ ' td').text("Container not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([0,1,0])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#db'+(i+1)+ ' td').text("Cover not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr == JSON.stringify([0,1,1])){
                    $('#wb'+(i+1)+ ' td').text("Not Loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-danger");
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
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([1,1,0])){
                    $('#db'+(i+1)+ ' td').text("Cover not loaded");
                    $('#wb'+(i+1)).removeClass("table-success");
                    $('#wb'+(i+1)).addClass("table-danger");
                    $('#db'+(i+1)).removeClass("table-success");
                    $('#db'+(i+1)).addClass("table-danger");
                }
                else if (check_arr  == JSON.stringify([1,1,1])){
                    $('#db'+(i+1)+ ' td').text("OK");
                    $('#wb'+(i+1)+ ' td').text("OK");
                    $('#wb'+(i+1)).removeClass("table-danger");
                    $('#wb'+(i+1)).addClass("table-success");
                    $('#db'+(i+1)).removeClass("table-danger");
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

function ChangeStage(){
    if(stage == 0){
        UpdateCheckConsumablesDiv()
    }
    if(stage == 1){
        UpdateCheckConsumablesDiv();
        UpdateCheckWetDryMagilDiv();   
    }
    id = stage_arr[stage];
    $('#' + id).removeClass("hide");
    HideOthersExcept(stage);
    
}

function CheckConsumables(){
    $('#status').text("Initializing...Please wait patiently");
    $.ajax({
        method:'GET',
        url:"/CheckConsumablesLoaded",
        success:function(respond){
            
        }
    });
    for(var i=0; i<6;i++){
        $('#wb'+(i+1)+ ' td').text("OK");
        $('#wb'+(i+1)).removeClass("table-danger");
        $('#wb'+(i+1)).removeClass("table-warning");
        $('#wb'+(i+1)).addClass("table-success");
        $('#db'+(i+1)+ ' td').text("OK");
        $('#db'+(i+1)).removeClass("table-danger");
        $('#db'+(i+1)).removeClass("table-warning");
        $('#db'+(i+1)).addClass("table-success");

    }
    

}

function CheckDryWetMagil(){
    // $('#CheckDryWetMagilBtn').hide();
    $('#status').text("Initializing...Please wait patiently");
    $.ajax({
        method:'GET',
        url:"/CheckDryWetMagil",
        success:function(respond){
            if (!CheckDryWetMagil_firstpress){
                console.log("reload");
                UpdateCheckWetDryMagilDiv();
            }
        }   
    });
    CheckDryWetMagil_firstpress = 0;
}

function StartProcess(){
    // $('#StartProcessBtn').hide();
    $.ajax({
        method:'GET',
        url:"/StartProcess",
        success:function(respond){
            $('#status').text("Initializing...Please wait patiently")
        }
    });
}