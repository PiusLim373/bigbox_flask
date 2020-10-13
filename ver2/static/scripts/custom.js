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

function CardHeaderSuccess(div_id){
    $('#' + div_id).append('<i class="fas fa-check-circle  align-right" id="greentick"></i>');
}

function UpdateCheckConsumablesDiv(){
    $.ajax({
        method:'POST',
        url:"/CheckConsumables",
        data:{
            'from':'webui'
        },
        success:function(respond){
            console.log(respond)
            if(respond['check_success'] == 1){
                $('#processfeedback').removeClass("bg-info");
                $('#processfeedback').removeClass("bg-danger");
                $('#processfeedback').addClass("bg-success");
                CardHeaderSuccess("checkconsumablescard");
                $('#checkconsumablescard').removeClass("card-header-danger");
                // $('#checkconsumablescard').addClass("card-header-success");
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
                $('#greentick').remove();
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

function Logout(){
    $.ajax({
        method:'GET',
        url:"/logout",
        success:function(respond){
            location.reload()
        }
    });
}

function StartNewProcess(){
    $.ajax({
        method:'GET',
        url:"/startnewprocess",
        success:function(respond){
            $('#StartNewProcess').addClass("hide");
        }
    });
}
function activateUR(){
     
    while(confirm("UR processed trigerred, please wait patiently...")){}
    // console.log("done waiting");
    return value;
}
function Refill(type){
    if(type =="RingSpareBay" || type == "NonRingSpareBay"){
        if (type == "RingSpareBay") {var InstList = ["ForcepArteryAdson", "ForcepArteryCrile", "HolderNeedleMayoHegar", "HolderNeedleCrilewood", "ForcepTissueLittlewood", "ForcepTissueStilles", "ForcepTissueBabcock", "ScissorDressingNurses", "ScissorMayo", "ScissorDissectingMetzenbaum", "ForcepSpongeHoldingRampley"];}
        else if (type == "NonRingSpareBay") {var InstList =["TowelClipJones", "ForcepDissectingGillies", "ForcepDissectingMcindoe", "HandleBardParker", "RulerGraduatedMultipurpose", "SpearRedivac"];}
        RefillDict = {}
        for(var i=0; i<InstList.length;i++){
            if ($('#' +InstList[i] +'Refill').val() != '0'){
                RefillDict[InstList[i]] = parseInt($('#' +InstList[i] +'Refill').val())
            }
        }
        if (Object.keys(RefillDict).length != 0){
            var i = 0
            var RefillMessage="You are about to refill: \n"
            for (const x in RefillDict){
                RefillMessage += RefillDict[x] + " x " + x + "\n";
                i ++;
            }
            RefillMessage += "This action cannot be undone, please confirm to add."
            if(confirm(RefillMessage)){
                $.ajax({
                    method:'POST',
                    url:"/RefillConsumables",
                    contentType: 'application/json',
                    data: JSON.stringify({
                        "module": type,
                        "action":"refill",
                        'value':RefillDict
                    }),
                    success:function(respond){
                        alert("Loading successful");
                        $("#" + type + "Modal").modal("hide");
                        CheckConsumables()
                    }
                });
            }
        }
        else{
            alert("Nothing is loaded")
            $("#" + type + "Modal").modal("hide");
        }
    }
    else if(type =="TempBrac"){
        $("#TempBracModal2").modal("show");
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": "TempBrac",
                "action":"reload"
            }),
            success:function(respond){
                alert("Loading successful");
                $("#TempBracModal2").modal("hide");
                $("#TempBracModal").modal("hide");
                CheckConsumables()
            }
        });
    }
    else if(type == "TrayPaperBay" || type == "IndicatorDispenser"|| type == "StickerTagPrinter"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": type,
                "action":"reload"
            }),
            success:function(respond){
                alert("Loading successful");
                $("#" + type + "Modal").modal("hide");
                CheckConsumables()
            }
        });
    }
    else if(type == "WrappingBayPaper"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": type,
                "action":"reload_paper"
            }),
            success:function(respond){
                alert("Loading successful");
                $("#" + type + "Modal").modal("hide");
                CheckConsumables()
            }
        });
    }
    else if(type == "WrappingBayTape"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": type,
                "action":"reload_tape"
            }),
            success:function(respond){
                alert("Loading successful");
                $("#" + type + "Modal").modal("hide");
                CheckConsumables()
            }
        });
    }
    else if(type == "PrinterBayWrapper"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": type,
                "action":"reload_wrapper"
            }),
            success:function(respond){
                alert("Loading successful");
                $("#" + type + "Modal").modal("hide");
                CheckConsumables()
            }
        });
    }
    else if(type == "PrinterBayA4Paper"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": type,
                "action":"reload_a4paper"
            }),
            success:function(respond){
                alert("Loading successful");
                $("#" + type + "Modal").modal("hide");
                CheckConsumables()
            }
        });
    }
    
}

function GETSpareBay(type){
    if (type == "RingSpareBay"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": "RingSpareBay",
                "action":"inst_count"
              }),
            success:function(respond){
                for(const x in respond){
                    if (respond[x] == 8){
                        $('#'+x+'Remaining').html("Number of " + x +" presents in Spare Bay: " + respond[x] + " <font color='green'> (Fully Loaded)</font");
                    }
                    else{
                        $('#'+x+'Remaining').html("Number of " + x +" presents in Spare Bay: " + respond[x]);
                    }
                    
                    var RefillString = ""
                    for (var i = 0; i <= 8 - respond[x]; i ++){
                        RefillString += "<option>" + i +"</option>"
                    }
                    $('#'+x+'Refill').html(RefillString);
                   
                }
            }
        });
    }
    else if (type == "NonRingSpareBay"){
        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": "NonRingSpareBay",
                "action":"inst_count"
              }),
            success:function(respond){
                for(const x in respond){
                    if (respond[x] == 8){           //This amount might not be 8
                        $('#'+x+'Remaining').html("Number of " + x +" presents in Spare Bay: " + respond[x] + " <font color='green'> (Fully Loaded)</font");
                    }
                    else{
                        $('#'+x+'Remaining').html("Number of " + x +" presents in Spare Bay: " + respond[x]);
                    }
                    
                    var RefillString = ""
                    for (var i = 0; i <= 8 - respond[x]; i ++){
                        RefillString += "<option>" + i +"</option>"
                    }
                    $('#'+x+'Refill').html(RefillString);
                   
                }
            }
        });
    }
}

function CollapseDropdown(type){
    if (!$('#' + type +'Collapse').hasClass('show')){
        $('#' + type +'CollapseDropdownBtn').removeClass('fa-chevron-down');
        $('#' + type +'CollapseDropdownBtn').addClass('fa-chevron-up');
    }
    else{
        $('#' + type +'CollapseDropdownBtn').removeClass('fa-chevron-up');
        $('#' + type +'CollapseDropdownBtn').addClass('fa-chevron-down');
    }
    if (type == 'RingSpareBay' || type == 'NonRingSpareBay'){
        GETSpareBay(type);
    }
    else if(type == 'TempBrac'){
        $('#CheckingBracModal').show();

        $.ajax({
            method:'POST',
            url:"/RefillConsumables",
            contentType: 'application/json',
            data: JSON.stringify({
                "module": "TempBrac",
                "action":"consumables_check"
              }),
            success:function(respond){
                console.log("returned!");
                if (respond == 'True'){
                    $("#CheckingBracModal").modal("hide");
                    console.log("hidden");
                    $('#TempBracCollapse1').collapse("show");
                }
                else{
                    $("#CheckingBracModal").modal("hide");
                    console.log("hidden");
                    $('#TempBracCollapse2').collapse("show")
                }
            }
        });
    }
    
}

function CollapseRefill(type){
    Refill(type);
    $('#' + type + 'Collapse').collapse("hide");
    $('#' + type +'CollapseDropdownBtn').removeClass('fa-chevron-up');
    $('#' + type +'CollapseDropdownBtn').addClass('fa-chevron-down');
}