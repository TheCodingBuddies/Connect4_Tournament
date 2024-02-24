using CsClient.Bots;

namespace CsClient.Bots
{
    public class FooBot : IBot
    {
        /// <inheritdoc/>
        public string Name { get; }

        /// <inheritdoc/>
        public int PlayerId { get; set; }

        /// <inheritdoc/>
        public int Play(int[][] field)
        {
            //
            // Do Your Fancy Stuff
            // field Array is current Board
            //
            // return welche Spalte du Bespielen magst.
            //
            // Beispiel.

            Random r = new Random();
            return r.Next(7);
        }

        public FooBot()
        {
            Name = "Example Name";      // Change
            PlayerId = -1;              // DO not Change
        }
    }
}
