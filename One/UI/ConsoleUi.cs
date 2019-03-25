using System;
using Utility;

namespace UI
{
    public class ConsoleUi
    {
        static void Main(string[] args)
        {
            Console.WriteLine("\n================================");
            var a = UserInput(1);
            var b = UserInput(2);
            var result = Utility.Utility.AreCoprime(a, b);
            Console.WriteLine($"{a} and {b} are{((result) ? "" : " not")} coprime numbers");
        }

        static int UserInput(int idx)
        {
            Console.WriteLine($"Enter positive integer number #{idx}:");
            while (true)
            {
                var str = Console.ReadLine().Trim();
                int val;
                if (int.TryParse(str, out val) && val >= 0)
                {
                    return val;
                }
                else
                {
                    Console.WriteLine($"Only positive integer allowed!");
                }
            }
        }
    }
}