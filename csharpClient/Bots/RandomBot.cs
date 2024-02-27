using CsClient.Bots;

namespace CsClient.Bots
{
    public class RandomBot : IBot
    {
        /// <inheritdoc/>
        public string Name { get; }

        /// <inheritdoc/>
        public int PlayerId { get; set; }

        /// <inheritdoc/>
        public int Play(int[][]? field)
        {
            Random r = new Random();
            return r.Next(7);
        }

        public RandomBot()
        {
            Name = "Random Bot";      
            PlayerId = -1;
        }
    }
}
