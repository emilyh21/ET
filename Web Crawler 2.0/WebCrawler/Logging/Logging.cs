﻿using System;
using System.Collections.Generic;
using System.Configuration;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace WebCrawler.Logging
{
    /// <summary>
    /// Logging class for Log functionality
    /// </summary>
    public static class Logging
    {
        /// <summary>
        /// Method to write reports to local machine.
        /// </summary>
        /// <param name="contents">string contents</param>
        public static void WriteReportToDisk(string contents)
        {
            string pathString2 = @"C:\Webpage";
            System.IO.Directory.CreateDirectory(pathString2);
            string fileNameX = "Output" + GLOBALS.numberofcrawl + ".html";
            string pathString = System.IO.Path.Combine(pathString2, fileNameX);
            //System.IO.File.Create(pathString);

            string fileName = pathString;
            FileStream fStream = null;
            if (File.Exists(fileName))
            {
                File.Delete(fileName);
                fStream = File.Create(fileName);
            }
            else
            {
                fStream = File.OpenWrite(fileName);
            }

            using (TextWriter writer = new StreamWriter(fStream))
            {
                writer.WriteLine(contents);
                writer.Flush();
            }

            fStream.Dispose();
        }
    }
}
