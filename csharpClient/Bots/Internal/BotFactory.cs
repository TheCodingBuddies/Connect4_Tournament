using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace CsClient.Bots.Internal
{
    public class BotFactory
    {
        public static IBot GetBotByName(string botName)
        {
            Assembly assembly = Assembly.GetExecutingAssembly();
            string className = $"{nameof(CsClient)}.{nameof(Bots)}.{botName}";
            
            Type type = assembly.GetType(className);
            if (type is null)
            {
                return new RandomBot();
            }
            else
            {
                return Activator.CreateInstance(type) as IBot;
            }
        }
    }
}
