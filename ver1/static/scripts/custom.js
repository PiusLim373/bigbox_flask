function GetStatus(){
    $.ajax({
		method:'GET',
		url:"/DebugPageStatus",
		success:function(response){
            console.log(response['shuttle'])
            for(var i = 0; i < 6; i++){
                if(response['tray'][i] == 1){
                    $('#TrayTrue' + (i+1)).addClass("selected");
                }
                else $('#TrayFalse' + (i+1)).addClass("selected")   
            }
            for(var i = 0; i < 6; i++){
                if(response['cover'][i] == 1){
                    $('#CoverTrue' + (i+1)).addClass("selected");
                }
                else $('#CoverFalse' + (i+1)).addClass("selected")   
            }
            for(var i = 0; i < 6; i++){
                if(response['container'][i] == 1){
                    $('#ContainerTrue' + (i+1)).addClass("selected");
                }
                else $('#ContainerFalse' + (i+1)).addClass("selected")   
            }
            for(var i = 0; i < 6; i++){
                if(response['shuttle'][i] == 1){
                    $('#ShuttleTrue' + (i+1)).addClass("selected");
                }
                else $('#ShuttleFalse' + (i+1)).addClass("selected")   
            }
            
		}
	});
}

function UpdateInput(item){
    json_data = $(item).data("json")
    console.log(json_data)
    console.log(json_data["type"])
    $.ajax({
		method:'POST',
        url:"/DebugPageStatus",
        contentType: 'application/json',
        data:JSON.stringify(json_data),
		success:function(response){
            console.log("ok")            
		}
	});
    console.log(json_data)
    console.log(json_data["type"])
}

function Nonringinput(){
    var arr = ['retractor1', 'retractor2', 'tcj1', 'tcj2', 'tcj3', 'tcj4', 'tcj5', 'tcj6', 'parker1', 'parker2', 'ruler', 'gillies', 'mcindoe', 'spear']
    var defective_arr = []
    for (var i = 0; i < 14; i++){
        if (!$('#' + arr[i])[0].checked){
            defective_arr.push(arr[i]);
        }
    }
    json_data = {'type':'nonring', 'value':defective_arr}
    $.ajax({
		method:'POST',
        url:"/DebugPageStatus",
        contentType: 'application/json',
        data:JSON.stringify(json_data),
		success:function(response){
            console.log("ok")            
		}
	});
    
    
}
