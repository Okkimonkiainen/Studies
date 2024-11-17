using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Xml.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Xml.Serialization;
using System.Xml;
using System.Xml.Xsl;


/*
 * Authors: Laura Siippainen and Tiina Tuomisto
 * Version: 2
 * Date: 11.12.2019
 */

namespace Harjoitustyo
{
    public partial class CompanyPersonnelData : Form
    {
        public List<Person> change;
        public List<Person> personneldata = new List<Person>();
        public List<string> postalcodecity;
        public bool edit = false;
        public bool ed = false;
        public bool del = false;
        public bool sav = false;
        public string username;
        public string time;
        public string edited = "Person details edited and saved. ";
        public string delete = "Person deleted. ";
        public string save = "New person saved. ";

        public CompanyPersonnelData()
        {
            InitializeComponent();
            personneldata = DeserializeXML();
            postalcodecity = new List<string>();
            dgvPersonnel.DataSource = null;
            dgvPersonnel.DataSource = personneldata;
            change= new List<Person>();

            //Editing and deleting employee information is only possible if dgvPersonnel.Datasource isn't empty
            if (dgvPersonnel.DataSource != null)
            {
                tsmiEdit.Enabled = true;
                btnDelete.Enabled = true;
                tsmiDelete.Enabled = true;
                btnEdit.Enabled = true;
                PostalCodeandCity();
            }
            else
            {
                tsmiEdit.Enabled = false;
                btnDelete.Enabled = false;
                tsmiDelete.Enabled = false;
                btnEdit.Enabled =false;

            }

        }
  
        //Getting all the values from column index 5 "PostalCodeCity" to create a suggestionlist
        public void PostalCodeandCity()
        {
            if (dgvPersonnel != null)
            {
                foreach (DataGridViewRow row in dgvPersonnel.Rows)
                {
                    foreach (DataGridViewCell cell in row.Cells)
                    {

                        if (cell.ColumnIndex == 5)
                        {
                            if (cell.Value != null)
                            {
                                string value = cell.Value.ToString();
                                postalcodecity.Add(value);
                            }
                        }
                    }
                }
            }
        }
        public List<Person> DeserializeXML()
        {
            if (File.Exists("c:\\temp\\Personnel.xml"))
            {
                dlgOpen.Filter = "XML-File|*.xml";
                dlgOpen.FileName = "c:\\temp\\Personnel.xml";
                using (StreamReader sr = new StreamReader(dlgOpen.FileName))
                {
                    XmlSerializer ser = new XmlSerializer(typeof(List<Person>));
                    object obj = ser.Deserialize(sr);
                    return (List<Person>)obj;
                }
            }
            else
            {
                return null;
            }
        }

        //Writing to a Log whenever the user has deleted, saved or edited employee information
        public void LogDetails(bool del, bool ed, bool sav)
        {
            time = DateTime.Now.ToString();
            username = Environment.UserName;
            StreamWriter sw = new StreamWriter("c:\\temp\\LogDetails.txt", true);

            if (del == true)
            {
                sw.WriteLine(username + " " + time + " " + delete);
                sw.Close();
            }
            else if (ed == true)
            {
                sw.WriteLine(username + " " + time + " " + edited);
                sw.Close();
            }
            else if (sav == true)
            {
                sw.WriteLine(username + " " + time + " " + save);
                sw.Close();
            }
        }

        //Deleting employee information
       private void btnDelete_Click(object sender, EventArgs e)
        {
            DialogResult answer = MessageBox.Show("Are you sure you want to delete?", "Delete folder", MessageBoxButtons.YesNo);

            if (answer == DialogResult.Yes)
            {
                if (dgvPersonnel.CurrentRow != null)
                {
                    try
                    {
                        XmlDocument xmldoc = new XmlDocument();
                        xmldoc.Load("c:\\temp\\Personnel.xml");

                        XmlNode xmlnode = xmldoc.DocumentElement.ChildNodes.Item(dgvPersonnel.CurrentRow.Index);
                        xmlnode.ParentNode.RemoveChild(xmlnode);
                        xmldoc.Save("c:\\temp\\Personnel.xml");

                        personneldata.RemoveAt(dgvPersonnel.CurrentRow.Index);
                        dgvPersonnel.DataSource = personneldata.ToList();
                        
                        del = true;
                        ed = false;
                        sav = false;
                        LogDetails(del, ed, sav);
                    }
                    catch (Exception)
                    {
                        MessageBox.Show("You have to choose a person to delete ", "Warning", MessageBoxButtons.OK);
                    }
                }

                if (personneldata.Count == 0)
                {
                    File.Delete("c:\\temp\\Personnel.xml");
                    personneldata = null;
                    dgvPersonnel.DataSource = null;
                    dgvPersonnel.DataSource = personneldata;
                    tsmiEdit.Enabled = false;
                    btnDelete.Enabled = false;
                    tsmiDelete.Enabled = false;
                    btnEdit.Enabled = false;
                }

            }
            else if (answer == DialogResult.No)
            {
                return;
            }

        }

        
        private void tsmiNew_Click(object sender, EventArgs e)
        {
            EmployeeData cpd = new EmployeeData(this);
            cpd.ShowDialog();
            PostalCodeandCity();
        }

        
        private void tsmiEdit_Click(object sender, EventArgs e)
        {
            edit = true;
            EmployeeData cpd = new EmployeeData(this);
            cpd.ShowDialog();
            PostalCodeandCity();
        }

        //Sorting columns: Callingname, Surname and Title if clicked
        private void Sort(string column, SortOrder sortOrder)
        {
            switch (column)
            {
                case "Callingname":
                    {
                        if (sortOrder == SortOrder.Ascending)
                        {
                            personneldata= personneldata.OrderBy(x => x.Callingname).ToList();
                            dgvPersonnel.DataSource = personneldata;

                        }
                        else
                        {
                            
                            personneldata = personneldata.OrderByDescending(x => x.Callingname).ToList();
                            dgvPersonnel.DataSource = personneldata;
                        }
                        break;
                    }
                case "Surname":
                    {
                        if (sortOrder == SortOrder.Ascending)
                        {
                            personneldata= personneldata.OrderBy(x => x.Surname).ToList();
                            dgvPersonnel.DataSource = personneldata;
                          
                        }
                        else
                        {
                            personneldata= personneldata.OrderByDescending(x => x.Surname).ToList();
                            dgvPersonnel.DataSource = personneldata;
                          
                        }
                        break;
                    }
                case "Title":
                    {
                        if (sortOrder == SortOrder.Ascending)
                        {
                            personneldata= personneldata.OrderBy(x => x.Title).ToList();
                            dgvPersonnel.DataSource = personneldata;
                          
                        }
                        else
                        {
                            personneldata= personneldata.OrderByDescending(x => x.Title).ToList();
                            dgvPersonnel.DataSource = personneldata;
                         
                        }
                        break;
                    }
            }
            SerializeXML("c:\\temp\\Personnel.xml", personneldata);
        }
        public void SerializeXML(string filename, List<Person> input)
        {
            XmlSerializer serializer = new XmlSerializer(input.GetType());

            using (var sw = new StreamWriter(filename))
            {
                serializer.Serialize(sw, input);
            }
        }

        private void dgvPersonnel_ColumnHeaderMouseClick(object sender, DataGridViewCellMouseEventArgs e)
        {
            DataGridView grid = (DataGridView)sender;
            SortOrder so = SortOrder.None;

            if (grid.Columns[e.ColumnIndex].HeaderCell.SortGlyphDirection == SortOrder.None || grid.Columns[e.ColumnIndex].HeaderCell.SortGlyphDirection == SortOrder.Ascending)
            {
                so = SortOrder.Descending;
            }
            else
            {
                so = SortOrder.Ascending;
            }
            Sort(grid.Columns[e.ColumnIndex].Name, so);
            grid.Columns[e.ColumnIndex].HeaderCell.SortGlyphDirection = so;
        }

        private void CompanyPersonnelData_FormClosing(object sender, FormClosingEventArgs e)
        {
            DialogResult answer = MessageBox.Show("Do you want to close this program?", "Closing the program", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

            if (answer == DialogResult.No)
            {
                e.Cancel = true;
            }
        }
    }
}

