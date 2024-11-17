package clientWS_NC;

import com.soap.ws.client.Calculator;
import com.soap.ws.client.CalculatorSoap;
import com.soap.ws.client.TempConvert;
import com.soap.ws.client.TempConvertSoap;

public class Health {

    public Health() {}
	
    //Fahrenheit and celsius convertions:
	public String convert2fahrenheit(String inputStr) {
		String celsius = inputStr;
		TempConvert service = new TempConvert();
		TempConvertSoap serviceSOAP = service.getTempConvertSoap();
		String result = serviceSOAP.celsiusToFahrenheit(celsius);
		//System.out.println(result);
		return result;
	}
    
	public String convert2celsius(String inputStr) {
		TempConvert NC_service = new TempConvert(); //created service object
		TempConvertSoap NC_serviceSOAP = NC_service.getTempConvertSoap();
		String result = NC_serviceSOAP.fahrenheitToCelsius(inputStr).toString();
		//System.out.println(result);
        return result;
	}
	
	//Calculator: height*height:
		public Integer Adding(Integer inputOne, Integer inputTwo) {
			//To test:
			System.out.println(inputOne +"and "+inputTwo);
			
			
			Calculator NC_service = new Calculator();
			CalculatorSoap NC_serviceSOAP = NC_service.getCalculatorSoap();
			int value = NC_serviceSOAP.multiply(inputOne, inputTwo); //returns 0			
			String res = Integer.toString(value);
			System.out.println(res); //returns 0
			
			//Because multiply -method gives a value of 0 for inputOne*inputTwo, so for demonstration:
			int multiply = inputOne*inputTwo;
			return multiply;
		}
}
