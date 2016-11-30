import org.apache.hadoop.hive.ql.exec.UDF;

public class Dict extends UDF{
	double distance;
	
	public double evaluate (double llat1, double llong1,double llat2,double llong2){
		//pi - число pi, rad - радиус сферы (Земли)
        int rad = 6372795;
        
        //в радианах
        double lat1 = llat1*Math.PI/180;
        double lat2 = llat2*Math.PI/180;
        double long1 = llong1*Math.PI/180;
        double long2 = llong2 * Math.PI / 180;

        double p = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin((lat2 - lat1) / 2), 2) + Math.cos(lat1) * Math.cos(lat2) * Math.pow(Math.sin(Math.abs(long2 - long1) / 2), 2)));
        distance = (p * rad);
        return distance;
	}
}
