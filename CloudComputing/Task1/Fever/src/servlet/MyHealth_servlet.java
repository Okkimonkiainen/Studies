package servlet;

import java.io.IOException;
import java.io.PrintWriter;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import clientWS_NC.Health;

/**
 * Servlet implementation class MyHealth_servlet
 */
@WebServlet("/MyHealth_servlet")
public class MyHealth_servlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public MyHealth_servlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		//response.getWriter().append("Served at: ").append(request.getContextPath());
		doPost(request, response); 
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		//doGet(request, response);
Health client = new Health();
		
		String value = request.getParameter("value").toString();
		String type = request.getParameter("type").toString();
		PrintWriter out = response.getWriter();
		if(value.equals("")){ 
			out.write("error: Please, provide a value!");  
		}else{
			String result = "";
			if(type.equals("celsius")) {
				//out.write(value);
				//result = client.convert2fahrenheit(value); //Error 301
				
				//For demonstration purposes, calculation of celsius to fahrenheit:
				Double a= Double.parseDouble(value);
				Double f = (a*1.8) + 32;
				out.write(f.toString());
				
			}else if(type.equals("fahrenheit")){
				//out.write(value);
				//result = client.convert2celsius(value); //Error 301
				
				//For demonstration purposes, calculation of fahrenheit to celsius:
				Double b= Double.parseDouble(value);
				Double c = (b-32)*0.5556;
				out.write(c.toString());
				
			}else if(type.equals("add")){
				//Part for height: height*height for calculation of BMI
				int valueOne = Integer.parseInt(value);
				int valueTwo= valueOne;
				int res;
				res = client.Adding(valueOne, valueTwo);
				result= Integer.toString(res);
				

			}else{
				//Fever:
				Double fever= Double.parseDouble(value);
				
				if(fever>50){ //For fahrenheit
					if(fever==99.14){
						out.write("Mild fever");
						
					}else if(fever>99.14 &&fever<100.4 ){
						out.write("Fever");
						
					}else if(fever>=100.4){
						out.write("High fever");
					}else{
						out.write("No fever or unlikely");	
					}
					
				}else{ //For celsius
					if(fever==37.3){
						out.write("Mild fever");
						
					}else if(fever>37.3 && fever<38){
						out.write("Fever");
						
					}else if(fever>=38){
						out.write("High fever");
					}else{
						out.write("No fever or unlikely");
						
					}
					
				}
				
				
				
			
				
			}
			out.write(result); 			
		}
					 
		out.flush();
	    out.close();

	}

	}


