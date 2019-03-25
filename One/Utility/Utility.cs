namespace Utility
{
    public class Utility
    {
        public static bool AreCoprime(int a, int b)
        {
           return (GCD(a, b) == 1);
        }

        public static int GCD(int a, int b)
        {
            // Everything divides 0 
            if (a == 0 || b == 0) 
                return 0; 
    
            // base case 
            if (a == b) 
                return a; 
    
            // a is greater 
            if (a > b) 
                return GCD(a-b, b); 
    
            return GCD(a, b-a); 
        }
    }
}