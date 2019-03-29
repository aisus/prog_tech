using System;
using Utility;

namespace UI
{
    public class ConsoleUi
    {
        static void Main(string[] args)
        {
            Console.WriteLine("\n==========COPRIME=NUMBERS==========\n");
            while (true)
            {
                var a = UserInput("A");
                var b = UserInput("B");
                var result = Utility.Utility.AreCoprime(a, b);
                Console.WriteLine($"{a} and {b} are{((result) ? "" : " not")} coprime numbers");
                Console.WriteLine("____________________________________\n");
            }
        }

        static int UserInput(string idx)
        {
            Console.WriteLine($"Enter non-negative integer number {idx}:");
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
                    Console.WriteLine($"Only non-negative integer allowed, try again");
                }
            }
        }
    }
}