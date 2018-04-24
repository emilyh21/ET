using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using WebCrawler.Repositories;

namespace WebCrawler
{
    public partial class UI : Form
    {
        public string website;
        // Declare our worker thread
        public Thread workerThread = null;
        private Crawler startCrawler = new Crawler(new ExternalUrlRepository(), new OtherUrlRepository(), new FailedUrlRepository(), new CurrentPageUrlRepository());
        public Crawler newCrawler;

        public UI()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            newCrawler = new Crawler(new ExternalUrlRepository(), new OtherUrlRepository(), new FailedUrlRepository(), new CurrentPageUrlRepository());
            website = textBox1.Text;
            GLOBALS.websiteURL = website;
            if (GLOBALS.websiteURL == "http://www.")
            {

            }
            else
            {
                label1.Text = "Web crawling started.";
                button2.Enabled = true;
                GLOBALS.crawl = true;
                this.workerThread = new Thread(new ThreadStart(newCrawler.InitializeCrawl));
                this.workerThread.Start();
            }
            
        }

        private void button2_Click(object sender, EventArgs e)
        {
            label2.Text = "Stopping Web crawling.";
            button2.Enabled = false;
            //GLOBALS.crawl = false;
            newCrawler.InitilizeCreateReport();
            this.workerThread.Abort();
        }
    }
}
