window.onload = customize;

function customize(){
	window.document.getElementById('div3').style.display = 'none';
}

function convertCelsius()
{
    window.document.getElementById('div3').style.display = 'none';
	var q_str = 'type=celsius&value='+document.getElementById('t1').value;
	doAjax('MyHealth_servlet',q_str,'convertCelsius_back','post',0);
}
function convertCelsius_back(result)
{
	if (result.substring(0,5)=='error'){
	   window.document.getElementById('div3').style.display = 'block';
	   window.document.getElementById('div3').innerHTML="<p style='color:red;'><b>"+result.substring(6)+"</b></p>";
   }else{
	   window.document.getElementById('t2').value=""+result;
   }
}

function convertFahrenheit()
{
    window.document.getElementById('div3').style.display = 'none';
	var q_str = 'type=fahrenheit&value='+document.getElementById('t3').value;
	doAjax('MyHealth_servlet',q_str,'convertFahrenheit_back','post',0);
}
function convertFahrenheit_back(result)
{
	if (result.substring(0,5)=='error'){
	   window.document.getElementById('div3').style.display = 'block';
	   window.document.getElementById('div3').innerHTML="<p style='color:red;'><b>"+result.substring(6)+"</b></p>";
   }else{
	   window.document.getElementById('t4').value=""+result;
   }
}

function convertFever()
{
    window.document.getElementById('div3').style.display = 'none';
	var q_str = 'type=fever&value='+document.getElementById('t5').value;
	doAjax('MyHealth_servlet',q_str,'convertFever_back','post',0);
}

function convertFever_back(result)
{
	if (result.substring(0,5)=='error'){
	   window.document.getElementById('div3').style.display = 'block';
	   window.document.getElementById('div3').innerHTML="<p style='color:red;'><b>"+result.substring(6)+"</b></p>";
   }else{
	   window.document.getElementById('t6').value=""+result;
   }
}

//CALCULATOR:
function doAdd()
{
    window.document.getElementById('div3').style.display = 'none';
	var q_str = 'type=add&value='+document.getElementById('t7').value;
	doAjax('MyHealth_servlet',q_str,'backAdd','post',0);
}

function backAdd(result)
{
	if (result.substring(0,5)=='error'){
	   window.document.getElementById('div3').style.display = 'block';
	   window.document.getElementById('div3').innerHTML="<p style='color:red;'><b>"+result.substring(6)+"</b></p>";
   }else{
	   window.document.getElementById('t8').value=""+result;
   }	

}

function doDivide()
{
    window.document.getElementById('div3').style.display = 'none';
	var q_str = 'type=divide&value='+document.getElementById('t9').value;
	doAjax('MyHealth_servlet',q_str,'backDivide','post',0);
}

function backDivide(result)
{
	if (result.substring(0,5)=='error'){
	   window.document.getElementById('div3').style.display = 'block';
	   window.document.getElementById('div3').innerHTML="<p style='color:red;'><b>"+result.substring(6)+"</b></p>";
   }else{
	   window.document.getElementById('t8').value=""+result;
   }	

}
function doBMI(textbox1, textbox2)
{
    window.document.getElementById('div3').style.display = 'none';
    
	var q_str = document.getElementById(textbox1).value;
	
	var q_str2 = document.getElementById(textbox2).value;
	
	var arvo = Math.round((q_str2/q_str)*10000);
	
	if(arvo<18.5){
		document.getElementById('t10').value = arvo +" Underweight";	
		
	}else if(arvo>=18.5 && arvo<=24.9){
		document.getElementById('t10').value = arvo +" Normal weight";
		
	}else if(arvo>=25 && arvo<=29.9){
		document.getElementById('t10').value = arvo +" Overweight";
		
	}else{
		document.getElementById('t10').value = arvo+" Obesity";
		
	}
	
	
	
	
	

}


