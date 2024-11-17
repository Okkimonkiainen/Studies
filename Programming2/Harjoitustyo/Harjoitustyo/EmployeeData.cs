using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.Xml.Serialization;
using System.Xml;

namespace Harjoitustyo
{
    public partial class EmployeeData : System.Windows.Forms.Form
    {
        List<string> postalcodeandcities;
        AutoCompleteStringCollection source;
        CompanyPersonnelData m_cp;
        int change, timer;
        

        public EmployeeData(CompanyPersonnelData cp)
        {
            InitializeComponent();

            m_cp = cp;

            cbJobTitle.Items.AddRange(new string[] { "Designer", "Manager", "Project employee", "Specialist", "Other" });
            cbJobDepartment.Items.AddRange(new string[] { "Design Deparment", "Planning Department", "Management Deparment", "Other" });
            postalcodeandcities = new List<string>();
            dtpStart.Format = DateTimePickerFormat.Short;
            dtpEnd.Format = DateTimePickerFormat.Short;
            source = new AutoCompleteStringCollection();
            sslStatus.Text = "";
            tsmiSave.Enabled = false;
            tsbtnSave.Enabled = false;
            change = 0; //variable for checking if user has saved after creating or editing employee information
            timer = 0;
        }

        //Saving the user input to a file when user creates a new employee or edits employee information
        //Enabling Edit and Delete -options on CompanyPersonnelData-form
        //Writing to the Log and adding postalcode and city to suggestion list
        private void tsbtnSave_Click(object sender, EventArgs e)
        {
            tmrSaved.Start();
            m_cp.tsmiEdit.Enabled = true;
            m_cp.btnDelete.Enabled = true;
            m_cp.btnEdit.Enabled = true;
            m_cp.tsmiDelete.Enabled = true;

            if (m_cp.personneldata == null)
            {
                m_cp.personneldata = new List<Person>();
            }
            Person p = new Person();
            if (m_cp.edit == true)
            {
                m_cp.del = false;
                m_cp.ed = true;
                m_cp.sav = false;
                m_cp.LogDetails(m_cp.del, m_cp.ed, m_cp.sav);
                int index = m_cp.dgvPersonnel.CurrentRow.Index;
                p.forenames = txtForenames.Text;
                p.surname = txtSurname.Text;
                p.callingname = txtCallingName.Text;
                p.jobtitle = cbJobTitle.Text;
                p.jobdepartment = cbJobDepartment.Text;
                p.socialsecuritynumber = txtSocialSecurity.Text;
                p.address = txtAddress.Text;
                p.jobstart = dtpStart.Text;
                if (cbContinuing.Checked)
                {
                    p.jobend = "Continuing";
                }
                else
                {
                    p.jobend = dtpEnd.Text;
                }
                p.postalcodecity = txtPostalCodeCity.Text;
                postalcodeandcities.Add(txtPostalCodeCity.Text);
                m_cp.personneldata[index] = p;
                m_cp.dgvPersonnel.DataSource = null;
                m_cp.dgvPersonnel.DataSource = m_cp.personneldata;
                
            }
            else if (m_cp.edit == false)
            {
                m_cp.del = false;
                m_cp.ed = false;
                m_cp.sav = true;
                m_cp.LogDetails(m_cp.del, m_cp.ed, m_cp.sav);

                p.forenames = txtForenames.Text;
                p.surname = txtSurname.Text;
                p.callingname = txtCallingName.Text;
                p.jobtitle = cbJobTitle.Text;
                p.jobdepartment = cbJobDepartment.Text;
                p.socialsecuritynumber = txtSocialSecurity.Text;
                p.address = txtAddress.Text;
                p.jobstart = dtpStart.Text;
                if (cbContinuing.Checked)
                {
                    p.jobend = "Continuing";
                }
                else
                {
                    p.jobend = dtpEnd.Text;
                }
                p.postalcodecity = txtPostalCodeCity.Text;
                postalcodeandcities.Add(txtPostalCodeCity.Text);
                if (m_cp.edit == false)
                {
                    m_cp.personneldata.Add(p);
                    m_cp.dgvPersonnel.DataSource = null;
                    m_cp.dgvPersonnel.DataSource = m_cp.personneldata;
                    ClearInput(this); //Clearing all user input
                    
                }   
            }

            foreach (string city in postalcodeandcities)
            {
                source.Add(city);
            }
            txtPostalCodeCity.AutoCompleteCustomSource = source;

            change = 0;
            tsbtnSave.Enabled = false;
            tsmiSave.Enabled = false;

            XmlDocument doc = new XmlDocument();
            dlgSave.Filter = "XML-File | *.xml";
            dlgSave.FileName = "c:\\temp\\Personnel.xml";
            try
            {
               
                m_cp.SerializeXML(dlgSave.FileName, m_cp.personneldata);
            }
            catch (Exception ex)
            {
                sslStatus.Text = "Error while saving the file " + ex;
            }
  
        }

        public void ClearInput(Control ctrl)
        {
            foreach(var c in ctrl.Controls)
            {
               if(c is TextBox)
                {
                    ((TextBox)c).Text = String.Empty;
                   
                }
               else if (c is DateTimePicker)
                {
                    ((DateTimePicker)c).Text = String.Empty;
                }
               else if (c is CheckBox)
                {
                    ((CheckBox)c).Checked = false;
                }
               else if (c is ComboBox)
                {
                    ((ComboBox)c).Text =String.Empty;
                }
            }
           
        }


        private void txtForenames_KeyPress(object sender, KeyPressEventArgs e)
        {
            if (Char.IsDigit(e.KeyChar) && e.KeyChar != '-' && e.KeyChar != ' ' && e.KeyChar != (char)8)
            {
                e.Handled = true;
            }
        }


        private void cbContinuing_CheckedChanged(object sender, EventArgs e)
        {
            tsmiSave.Enabled = true;
            tsbtnSave.Enabled = true;

            change = 1;

            if (cbContinuing.Checked)
            {
                dtpEnd.Enabled = false;
            }
            else
            {
                dtpEnd.Enabled = true;
            }
        }

        //Creating a suggestlist for PostalCode and City-textbox according to previous user input in dgvPersonnel
        //Showing the previous information of the chosen employee if the user wants to edit their information
        private void EmployeeData_Load(object sender, EventArgs e)
        {
            foreach (string city in m_cp.postalcodecity)
            {
                source.Add(city);
            }

            txtPostalCodeCity.AutoCompleteMode = AutoCompleteMode.SuggestAppend;
            txtPostalCodeCity.AutoCompleteSource = AutoCompleteSource.CustomSource;
            txtPostalCodeCity.AutoCompleteCustomSource = source;

            if (m_cp.edit == true)
            {
                if (m_cp.dgvPersonnel.CurrentRow.Index != -1)
                {
                    txtForenames.Text = m_cp.dgvPersonnel.CurrentRow.Cells[0].Value.ToString();
                    txtSurname.Text = m_cp.dgvPersonnel.CurrentRow.Cells[1].Value.ToString();
                    txtCallingName.Text = m_cp.dgvPersonnel.CurrentRow.Cells[2].Value.ToString();
                    txtSocialSecurity.Text = m_cp.dgvPersonnel.CurrentRow.Cells[3].Value.ToString();
                    txtAddress.Text = m_cp.dgvPersonnel.CurrentRow.Cells[4].Value.ToString();
                    txtPostalCodeCity.Text = m_cp.dgvPersonnel.CurrentRow.Cells[5].Value.ToString();
                    dtpStart.Text = m_cp.dgvPersonnel.CurrentRow.Cells[6].Value.ToString();
                    if (m_cp.dgvPersonnel.CurrentRow.Cells[7].Value.ToString() == "Continuing")
                    {
                        cbContinuing.Checked = true;
                    }
                    else
                    {
                        dtpEnd.Text = m_cp.dgvPersonnel.CurrentRow.Cells[7].Value.ToString();
                    }
                    cbJobTitle.Text = m_cp.dgvPersonnel.CurrentRow.Cells[8].Value.ToString();
                    cbJobDepartment.Text = m_cp.dgvPersonnel.CurrentRow.Cells[9].Value.ToString();
                    change = 0;
                }
                tsbtnSave.Enabled = false;
                tsmiSave.Enabled = false;
            }
        }

        private void EmployeeData_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (change > 0 )
            {
                DialogResult answer = MessageBox.Show("Do you want to close this form without saving the changes?", "Closing the form", MessageBoxButtons.YesNo, MessageBoxIcon.Warning);

                if (answer == DialogResult.No)
                {
                    e.Cancel = true;
                }
            }
            m_cp.edit = false;

        }

        //Validation of Social Security Number
        private void txtSocialSecurity_Validated(object sender, EventArgs e)
        {
            errorProvider.SetError(txtSocialSecurity, "");
        }

        private void txtSocialSecurity_Validating(object sender, CancelEventArgs e)
        {
            string errMsg = "";
            if (SSD(txtSocialSecurity.Text, out errMsg) == false)
            {
                e.Cancel = true;
                txtSocialSecurity.SelectAll();
                errorProvider.SetError(txtSocialSecurity, errMsg);
            }
        }
        private bool SSD(string hetu, out string errMsg) 
        {
            errMsg = "";
            bool ret = true;

            string tmp;
            string tarkiste = "0123456789ABCDEFHJKLMNPRSTUVWXY";
            int jj = 0;
            int luku = 0;

            hetu = txtSocialSecurity.Text;
            tmp = hetu;

            try
            {
                tmp = tmp.Remove(6, 1);
                tmp = tmp.Remove(9, 1);
                int.TryParse(tmp, out luku);
                jj = luku % 31;
            }
            catch (Exception)
            {
                errMsg = "Invalid Social Security Number ";
                ret = false;
            }
            try
            {
                if (hetu[10] == tarkiste[jj])
                {
                    ret = true;
                }
            }
            catch
            {
                errMsg = "Invalid Social Security Number";
                ret = false;
            }
            return ret;
        }

        private void tmrSaved_Tick(object sender, EventArgs e)
        {
            timer++;
            if(timer<=5)
            {
                sslStatus.Text = "Saved Succesfully";
                
            }
            else if (timer > 5)
            {
                sslStatus.Text = "";
                timer = 0;
                tmrSaved.Stop();
            }
            
        }
    }

}
