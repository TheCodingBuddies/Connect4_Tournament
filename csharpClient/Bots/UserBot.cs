using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace CsClient.Bots
{
    public class UserBot : IBot
    {
        /// <inheritdoc/>
        public string Name { get; }

        /// <inheritdoc/>
        public int PlayerId { get; set; }

        /// <inheritdoc/>
        public int Play(int[][] field)
        {
            //
            // Deine Play Methode - hier kann deine Logik stehen :)
            // 

            return 0;
        }

        public UserBot()
        {
            Name = "FOOBAR";      // Change
            PlayerId = -1;        // DO not Change
        }
    }
}
