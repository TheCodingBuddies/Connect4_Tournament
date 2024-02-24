using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

// ns is not corret, that is intendet
namespace CsClient.Bots
{
    public interface IBot
    {
        /// <summary>
        /// Playerid, diese wird vom Server vergeben, bitte mit -1 initialisieren.
        /// </summary>
        int PlayerId { get; set; }
        /// <summary>
        /// Name des Spielers.
        /// </summary>
        string Name { get; }
        /// <summary>
        /// Spielmethode.
        /// </summary>
        /// <param name="field"></param>
        /// <returns>Spalte welche bespielt werden soll</returns>
        int Play(int[][] field);

    }
}
