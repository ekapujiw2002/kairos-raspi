function faceAPISend(cmdin, datax){
	bootbox.dialog({ message: '<div class="text-center"><i class="glyphicon glyphicon-refresh"></i> Processing...</div>', size:'small' });
	
	$.getJSON(
		'face',
		{
			'c':cmdin,
			'n':datax
		},
		function(datax){

			bootbox.hideAll();

			if (typeof datax.cmd !== "undefined"){
				if (typeof datax.error !== "undefined"){
					bootbox.alert({
						title: 'ERROR',
						message: datax.error,
						size: 'small'
					});
				}
				else{	
					//console.log(datax);
					switch(datax.cmd){
						case 1:
							if (typeof datax.cnt !== "undefined"){
								if(datax.cnt != 0){	
									//alert('Subject ID = ' + datax.result.subject_id+'\nConfidence = '+ (Math.round(datax.result.confidence*100)) +'%');
									
									bootbox.alert({
										title: 'SUCCESS',
										message: 'Subject ID = ' + datax.result.subject_id+'<br/>Confidence = '+ (Math.round(datax.result.confidence*100)) +'%',
										size: 'small'
									});
								}
								else{
									bootbox.alert({
										title: 'ERROR',
										message: 'No face recognize',
										size: 'small'
									});
								}
							}
							break;
							
						case 2:
							if(datax.cnt != 0){	
								//alert('New face added');
								bootbox.alert({
										title: 'SUCCESS',
										message: 'New face added',
										size: 'small'
									});
							}
							else{
								bootbox.alert({
									title: 'ERROR',
									message: 'Cannot add new face!!!',
									size: 'small'
								});
							}
							break;
							
						case 3:
							if(datax.cnt != 0){	
								bootbox.alert({
										title: 'SUCCESS',
										message: 'All faces cleared',
										size: 'small'
									});
							}
							else{
								bootbox.alert({
									title: 'ERROR',
									message: 'Cannot clear all faces!!!',
									size: 'small'
								});
							}
							break;
							
						case 4:
							//console.log(datax);
							
							if(datax.cnt != 0){	
								var list_subject = '<ul class="list-group">';
								$.each(
									datax.subjects,
									function(id, value){
										list_subject += '<li class="list-group-item">'+value+'</li>';
									}
								);
								list_subject += '</ul>';
								
								bootbox.alert({
										title: 'SUBJECTS',
										message: list_subject,
										size: 'small'
									});
							}
							else{
								bootbox.alert({
									title: 'ERROR',
									message: 'No faces found!!!',
									size: 'small'
								});
							}
							break;
							
						default:
							bootbox.alert({
								title: 'ERROR',
								message: 'Unknown command',
								size: 'small'
							});
							break;
					}	
				}					
			}
		}
	)
	.error(
		function(){
			bootbox.hideAll();
		}
	);
}

function faceCommand(acmd){
		var galeri = 'tes1';
		var cmdin = parseInt(acmd);
		
		switch(cmdin){
			case 1:
				faceAPISend(cmdin, galeri);
				break;
				
			case 2:
				bootbox.prompt({ 
					size: "small",
					title: "Subject name :", 
					callback: function(result){
						if(result){
							//console.log(result.trim());
							if(result.trim()!=''){
								//bootbox.alert(result);
								faceAPISend(cmdin, result);
							}
							else{
								bootbox.dialog({
									title:'ERROR',
									size:'small',
									message:'No subject name given'
								}
								);
							}
						}
					}
				});
				break;
				
			case 3:
				bootbox.confirm({ 
					title: "CLEAR",
					size: "small",
					message: "Clear all saved faces?", 
					callback: function(result){
						if(result){
							faceAPISend(cmdin, galeri);
						}
					}
				});
				break;
				
			case 4:
				faceAPISend(cmdin, galeri);
				break;
		}		
	}
	
function ChangeRes(w, h){
        var data = new FormData();
        data.append('width', w);
        data.append('height', h);

        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/setparams', true);
        xhr.send(data);
    }	
	
$(document).ready(function(){	

    //$(':checkbox').checkboxpicker();
	
	$('[data-toggle="tooltip"]').tooltip();

    

    $("#low").click(function(){
        ChangeRes(320, 240);
	})

	$("#norm").click(function(){
        ChangeRes(640, 480);
	})

	$("#hi").click(function(){
        ChangeRes(800, 600);
	})

	$(':checkbox').checkboxpicker().change(function() {
        if($('input[name="agree"]:checked').length > 0) {
            document.getElementById("videofield").src="video_feed?fd=true";
        }
        else{
            document.getElementById("videofield").src="video_feed?fd=false";
        }
    });
});