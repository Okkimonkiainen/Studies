namespace Harjoitustyo
{
    partial class EmployeeData
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(EmployeeData));
            this.msFile = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.tsmiSave = new System.Windows.Forms.ToolStripMenuItem();
            this.tsShortcuts = new System.Windows.Forms.ToolStrip();
            this.tsbtnSave = new System.Windows.Forms.ToolStripButton();
            this.lblPersonalData = new System.Windows.Forms.Label();
            this.lblEmploymentData = new System.Windows.Forms.Label();
            this.lblForenames = new System.Windows.Forms.Label();
            this.lblSocialSecurity = new System.Windows.Forms.Label();
            this.lblCallingName = new System.Windows.Forms.Label();
            this.lblSurname = new System.Windows.Forms.Label();
            this.txtForenames = new System.Windows.Forms.TextBox();
            this.txtSurname = new System.Windows.Forms.TextBox();
            this.txtSocialSecurity = new System.Windows.Forms.TextBox();
            this.txtCallingName = new System.Windows.Forms.TextBox();
            this.lblPostalCode = new System.Windows.Forms.Label();
            this.lblAddress = new System.Windows.Forms.Label();
            this.lblHomeAddress = new System.Windows.Forms.Label();
            this.txtAddress = new System.Windows.Forms.TextBox();
            this.txtPostalCodeCity = new System.Windows.Forms.TextBox();
            this.dtpStart = new System.Windows.Forms.DateTimePicker();
            this.dtpEnd = new System.Windows.Forms.DateTimePicker();
            this.lblJobEnd = new System.Windows.Forms.Label();
            this.lblJobStart = new System.Windows.Forms.Label();
            this.lblJobTitle = new System.Windows.Forms.Label();
            this.cbJobTitle = new System.Windows.Forms.ComboBox();
            this.lblJobDepartment = new System.Windows.Forms.Label();
            this.cbJobDepartment = new System.Windows.Forms.ComboBox();
            this.dlgSave = new System.Windows.Forms.SaveFileDialog();
            this.dlgEdit = new System.Windows.Forms.OpenFileDialog();
            this.cbContinuing = new System.Windows.Forms.CheckBox();
            this.ssStatusStrip = new System.Windows.Forms.StatusStrip();
            this.sslStatus = new System.Windows.Forms.ToolStripStatusLabel();
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.errorProvider = new System.Windows.Forms.ErrorProvider(this.components);
            this.tmrSaved = new System.Windows.Forms.Timer(this.components);
            this.helpProvider = new System.Windows.Forms.HelpProvider();
            this.msFile.SuspendLayout();
            this.tsShortcuts.SuspendLayout();
            this.ssStatusStrip.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.errorProvider)).BeginInit();
            this.SuspendLayout();
            // 
            // msFile
            // 
            this.msFile.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.msFile.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem});
            this.msFile.Location = new System.Drawing.Point(0, 0);
            this.msFile.Name = "msFile";
            this.msFile.Padding = new System.Windows.Forms.Padding(5, 2, 0, 2);
            this.msFile.Size = new System.Drawing.Size(963, 28);
            this.msFile.TabIndex = 0;
            this.msFile.Text = "File";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.tsmiSave});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(46, 24);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // tsmiSave
            // 
            this.tsmiSave.Name = "tsmiSave";
            this.tsmiSave.ShortcutKeys = ((System.Windows.Forms.Keys)((System.Windows.Forms.Keys.Control | System.Windows.Forms.Keys.S)));
            this.tsmiSave.Size = new System.Drawing.Size(224, 26);
            this.tsmiSave.Text = "Save";
            this.tsmiSave.Click += new System.EventHandler(this.tsbtnSave_Click);
            // 
            // tsShortcuts
            // 
            this.tsShortcuts.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.tsShortcuts.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.tsbtnSave});
            this.tsShortcuts.Location = new System.Drawing.Point(0, 28);
            this.tsShortcuts.Name = "tsShortcuts";
            this.tsShortcuts.Size = new System.Drawing.Size(963, 27);
            this.tsShortcuts.TabIndex = 1;
            // 
            // tsbtnSave
            // 
            this.tsbtnSave.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Image;
            this.tsbtnSave.Image = ((System.Drawing.Image)(resources.GetObject("tsbtnSave.Image")));
            this.tsbtnSave.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.tsbtnSave.Name = "tsbtnSave";
            this.tsbtnSave.Size = new System.Drawing.Size(29, 24);
            this.tsbtnSave.Text = "Save";
            this.tsbtnSave.Click += new System.EventHandler(this.tsbtnSave_Click);
            // 
            // lblPersonalData
            // 
            this.lblPersonalData.AutoSize = true;
            this.lblPersonalData.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblPersonalData.Location = new System.Drawing.Point(13, 76);
            this.lblPersonalData.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblPersonalData.Name = "lblPersonalData";
            this.lblPersonalData.Size = new System.Drawing.Size(100, 20);
            this.lblPersonalData.TabIndex = 2;
            this.lblPersonalData.Text = "Personal Data";
            // 
            // lblEmploymentData
            // 
            this.lblEmploymentData.AutoSize = true;
            this.lblEmploymentData.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblEmploymentData.Location = new System.Drawing.Point(13, 359);
            this.lblEmploymentData.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblEmploymentData.Name = "lblEmploymentData";
            this.lblEmploymentData.Size = new System.Drawing.Size(129, 20);
            this.lblEmploymentData.TabIndex = 3;
            this.lblEmploymentData.Text = "Employment Data";
            // 
            // lblForenames
            // 
            this.lblForenames.AutoSize = true;
            this.lblForenames.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblForenames.Location = new System.Drawing.Point(17, 116);
            this.lblForenames.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblForenames.Name = "lblForenames";
            this.lblForenames.Size = new System.Drawing.Size(81, 20);
            this.lblForenames.TabIndex = 4;
            this.lblForenames.Text = "Forenames";
            // 
            // lblSocialSecurity
            // 
            this.lblSocialSecurity.AutoSize = true;
            this.lblSocialSecurity.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblSocialSecurity.Location = new System.Drawing.Point(457, 154);
            this.lblSocialSecurity.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblSocialSecurity.Name = "lblSocialSecurity";
            this.lblSocialSecurity.Size = new System.Drawing.Size(163, 20);
            this.lblSocialSecurity.TabIndex = 5;
            this.lblSocialSecurity.Text = "Social Security Number";
            // 
            // lblCallingName
            // 
            this.lblCallingName.AutoSize = true;
            this.lblCallingName.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblCallingName.Location = new System.Drawing.Point(457, 116);
            this.lblCallingName.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblCallingName.Name = "lblCallingName";
            this.lblCallingName.Size = new System.Drawing.Size(99, 20);
            this.lblCallingName.TabIndex = 6;
            this.lblCallingName.Text = "Calling Name";
            // 
            // lblSurname
            // 
            this.lblSurname.AutoSize = true;
            this.lblSurname.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblSurname.Location = new System.Drawing.Point(17, 154);
            this.lblSurname.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblSurname.Name = "lblSurname";
            this.lblSurname.Size = new System.Drawing.Size(67, 20);
            this.lblSurname.TabIndex = 7;
            this.lblSurname.Text = "Surname";
            // 
            // txtForenames
            // 
            this.txtForenames.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtForenames.Location = new System.Drawing.Point(180, 113);
            this.txtForenames.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtForenames.Name = "txtForenames";
            this.txtForenames.Size = new System.Drawing.Size(188, 27);
            this.txtForenames.TabIndex = 8;
            this.txtForenames.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            this.txtForenames.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.txtForenames_KeyPress);
            // 
            // txtSurname
            // 
            this.txtSurname.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtSurname.Location = new System.Drawing.Point(180, 151);
            this.txtSurname.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtSurname.Name = "txtSurname";
            this.txtSurname.Size = new System.Drawing.Size(188, 27);
            this.txtSurname.TabIndex = 9;
            this.txtSurname.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            this.txtSurname.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.txtForenames_KeyPress);
            // 
            // txtSocialSecurity
            // 
            this.txtSocialSecurity.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtSocialSecurity.Location = new System.Drawing.Point(664, 151);
            this.txtSocialSecurity.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtSocialSecurity.MaxLength = 11;
            this.txtSocialSecurity.Name = "txtSocialSecurity";
            this.txtSocialSecurity.Size = new System.Drawing.Size(188, 27);
            this.txtSocialSecurity.TabIndex = 11;
            this.txtSocialSecurity.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            this.txtSocialSecurity.Validating += new System.ComponentModel.CancelEventHandler(this.txtSocialSecurity_Validating);
            this.txtSocialSecurity.Validated += new System.EventHandler(this.txtSocialSecurity_Validated);
            // 
            // txtCallingName
            // 
            this.txtCallingName.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtCallingName.Location = new System.Drawing.Point(664, 113);
            this.txtCallingName.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtCallingName.Name = "txtCallingName";
            this.txtCallingName.Size = new System.Drawing.Size(188, 27);
            this.txtCallingName.TabIndex = 10;
            this.txtCallingName.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            this.txtCallingName.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.txtForenames_KeyPress);
            // 
            // lblPostalCode
            // 
            this.lblPostalCode.AutoSize = true;
            this.lblPostalCode.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblPostalCode.Location = new System.Drawing.Point(16, 299);
            this.lblPostalCode.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblPostalCode.Name = "lblPostalCode";
            this.lblPostalCode.Size = new System.Drawing.Size(145, 20);
            this.lblPostalCode.TabIndex = 13;
            this.lblPostalCode.Text = "Postal Code and City";
            // 
            // lblAddress
            // 
            this.lblAddress.AutoSize = true;
            this.lblAddress.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblAddress.Location = new System.Drawing.Point(17, 260);
            this.lblAddress.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblAddress.Name = "lblAddress";
            this.lblAddress.Size = new System.Drawing.Size(62, 20);
            this.lblAddress.TabIndex = 14;
            this.lblAddress.Text = "Address";
            // 
            // lblHomeAddress
            // 
            this.lblHomeAddress.AutoSize = true;
            this.lblHomeAddress.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Underline, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblHomeAddress.Location = new System.Drawing.Point(13, 222);
            this.lblHomeAddress.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblHomeAddress.Name = "lblHomeAddress";
            this.lblHomeAddress.Size = new System.Drawing.Size(107, 20);
            this.lblHomeAddress.TabIndex = 15;
            this.lblHomeAddress.Text = "Home Address";
            // 
            // txtAddress
            // 
            this.txtAddress.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtAddress.Location = new System.Drawing.Point(180, 257);
            this.txtAddress.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtAddress.Name = "txtAddress";
            this.txtAddress.Size = new System.Drawing.Size(188, 27);
            this.txtAddress.TabIndex = 16;
            this.txtAddress.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // txtPostalCodeCity
            // 
            this.txtPostalCodeCity.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.txtPostalCodeCity.Location = new System.Drawing.Point(180, 296);
            this.txtPostalCodeCity.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.txtPostalCodeCity.Name = "txtPostalCodeCity";
            this.txtPostalCodeCity.Size = new System.Drawing.Size(188, 27);
            this.txtPostalCodeCity.TabIndex = 18;
            this.txtPostalCodeCity.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // dtpStart
            // 
            this.dtpStart.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.dtpStart.Location = new System.Drawing.Point(113, 395);
            this.dtpStart.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.dtpStart.Name = "dtpStart";
            this.dtpStart.Size = new System.Drawing.Size(265, 27);
            this.dtpStart.TabIndex = 19;
            this.dtpStart.ValueChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // dtpEnd
            // 
            this.dtpEnd.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.dtpEnd.Location = new System.Drawing.Point(113, 435);
            this.dtpEnd.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.dtpEnd.Name = "dtpEnd";
            this.dtpEnd.Size = new System.Drawing.Size(265, 27);
            this.dtpEnd.TabIndex = 20;
            this.dtpEnd.ValueChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // lblJobEnd
            // 
            this.lblJobEnd.AutoSize = true;
            this.lblJobEnd.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblJobEnd.Location = new System.Drawing.Point(17, 438);
            this.lblJobEnd.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblJobEnd.Name = "lblJobEnd";
            this.lblJobEnd.Size = new System.Drawing.Size(61, 20);
            this.lblJobEnd.TabIndex = 21;
            this.lblJobEnd.Text = "Job End";
            // 
            // lblJobStart
            // 
            this.lblJobStart.AutoSize = true;
            this.lblJobStart.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblJobStart.Location = new System.Drawing.Point(17, 398);
            this.lblJobStart.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblJobStart.Name = "lblJobStart";
            this.lblJobStart.Size = new System.Drawing.Size(67, 20);
            this.lblJobStart.TabIndex = 22;
            this.lblJobStart.Text = "Job Start";
            // 
            // lblJobTitle
            // 
            this.lblJobTitle.AutoSize = true;
            this.lblJobTitle.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblJobTitle.Location = new System.Drawing.Point(457, 398);
            this.lblJobTitle.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblJobTitle.Name = "lblJobTitle";
            this.lblJobTitle.Size = new System.Drawing.Size(65, 20);
            this.lblJobTitle.TabIndex = 23;
            this.lblJobTitle.Text = "Job Title";
            // 
            // cbJobTitle
            // 
            this.cbJobTitle.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.cbJobTitle.FormattingEnabled = true;
            this.cbJobTitle.Location = new System.Drawing.Point(664, 395);
            this.cbJobTitle.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.cbJobTitle.Name = "cbJobTitle";
            this.cbJobTitle.Size = new System.Drawing.Size(188, 28);
            this.cbJobTitle.TabIndex = 24;
            this.cbJobTitle.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // lblJobDepartment
            // 
            this.lblJobDepartment.AutoSize = true;
            this.lblJobDepartment.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.lblJobDepartment.Location = new System.Drawing.Point(457, 438);
            this.lblJobDepartment.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.lblJobDepartment.Name = "lblJobDepartment";
            this.lblJobDepartment.Size = new System.Drawing.Size(116, 20);
            this.lblJobDepartment.TabIndex = 25;
            this.lblJobDepartment.Text = "Job Department";
            // 
            // cbJobDepartment
            // 
            this.cbJobDepartment.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.cbJobDepartment.FormattingEnabled = true;
            this.cbJobDepartment.Location = new System.Drawing.Point(664, 435);
            this.cbJobDepartment.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.cbJobDepartment.Name = "cbJobDepartment";
            this.cbJobDepartment.Size = new System.Drawing.Size(188, 28);
            this.cbJobDepartment.TabIndex = 26;
            this.cbJobDepartment.TextChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // dlgEdit
            // 
            this.dlgEdit.FileName = "Personnel";
            // 
            // cbContinuing
            // 
            this.cbContinuing.AutoSize = true;
            this.cbContinuing.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.cbContinuing.Location = new System.Drawing.Point(113, 468);
            this.cbContinuing.Margin = new System.Windows.Forms.Padding(3, 2, 3, 2);
            this.cbContinuing.Name = "cbContinuing";
            this.cbContinuing.Size = new System.Drawing.Size(103, 24);
            this.cbContinuing.TabIndex = 28;
            this.cbContinuing.Text = "Continuing";
            this.cbContinuing.UseVisualStyleBackColor = true;
            this.cbContinuing.CheckedChanged += new System.EventHandler(this.cbContinuing_CheckedChanged);
            // 
            // ssStatusStrip
            // 
            this.ssStatusStrip.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.ssStatusStrip.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.sslStatus});
            this.ssStatusStrip.Location = new System.Drawing.Point(0, 569);
            this.ssStatusStrip.Name = "ssStatusStrip";
            this.ssStatusStrip.Padding = new System.Windows.Forms.Padding(1, 0, 13, 0);
            this.ssStatusStrip.Size = new System.Drawing.Size(963, 26);
            this.ssStatusStrip.TabIndex = 29;
            // 
            // sslStatus
            // 
            this.sslStatus.Name = "sslStatus";
            this.sslStatus.Size = new System.Drawing.Size(49, 20);
            this.sslStatus.Text = "Status";
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.ImageScalingSize = new System.Drawing.Size(20, 20);
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(61, 4);
            // 
            // errorProvider
            // 
            this.errorProvider.ContainerControl = this;
            // 
            // tmrSaved
            // 
            this.tmrSaved.Interval = 500;
            this.tmrSaved.Tick += new System.EventHandler(this.tmrSaved_Tick);
            // 
            // EmployeeData
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(963, 595);
            this.Controls.Add(this.ssStatusStrip);
            this.Controls.Add(this.cbContinuing);
            this.Controls.Add(this.cbJobDepartment);
            this.Controls.Add(this.lblJobDepartment);
            this.Controls.Add(this.cbJobTitle);
            this.Controls.Add(this.lblJobTitle);
            this.Controls.Add(this.lblJobStart);
            this.Controls.Add(this.lblJobEnd);
            this.Controls.Add(this.dtpEnd);
            this.Controls.Add(this.dtpStart);
            this.Controls.Add(this.txtPostalCodeCity);
            this.Controls.Add(this.txtAddress);
            this.Controls.Add(this.lblHomeAddress);
            this.Controls.Add(this.lblAddress);
            this.Controls.Add(this.lblPostalCode);
            this.Controls.Add(this.txtCallingName);
            this.Controls.Add(this.txtSocialSecurity);
            this.Controls.Add(this.txtSurname);
            this.Controls.Add(this.txtForenames);
            this.Controls.Add(this.lblSurname);
            this.Controls.Add(this.lblCallingName);
            this.Controls.Add(this.lblSocialSecurity);
            this.Controls.Add(this.lblForenames);
            this.Controls.Add(this.lblEmploymentData);
            this.Controls.Add(this.lblPersonalData);
            this.Controls.Add(this.tsShortcuts);
            this.Controls.Add(this.msFile);
            this.MainMenuStrip = this.msFile;
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.Name = "EmployeeData";
            this.Text = "Employee Data";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.EmployeeData_FormClosing);
            this.Load += new System.EventHandler(this.EmployeeData_Load);
            this.msFile.ResumeLayout(false);
            this.msFile.PerformLayout();
            this.tsShortcuts.ResumeLayout(false);
            this.tsShortcuts.PerformLayout();
            this.ssStatusStrip.ResumeLayout(false);
            this.ssStatusStrip.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.errorProvider)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        
        
        private System.Windows.Forms.MenuStrip msFile;
        private System.Windows.Forms.ToolStripMenuItem fileToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem tsmiSave;
        private System.Windows.Forms.ToolStrip tsShortcuts;
        private System.Windows.Forms.ToolStripButton tsbtnSave;
        private System.Windows.Forms.Label lblPersonalData;
        private System.Windows.Forms.Label lblEmploymentData;
        private System.Windows.Forms.Label lblForenames;
        private System.Windows.Forms.Label lblSocialSecurity;
        private System.Windows.Forms.Label lblCallingName;
        private System.Windows.Forms.Label lblSurname;
        private System.Windows.Forms.TextBox txtForenames;
        private System.Windows.Forms.TextBox txtSurname;
        private System.Windows.Forms.TextBox txtSocialSecurity;
        private System.Windows.Forms.TextBox txtCallingName;
        private System.Windows.Forms.Label lblPostalCode;
        private System.Windows.Forms.Label lblAddress;
        private System.Windows.Forms.Label lblHomeAddress;
        private System.Windows.Forms.TextBox txtAddress;
        private System.Windows.Forms.TextBox txtPostalCodeCity;
        private System.Windows.Forms.DateTimePicker dtpStart;
        private System.Windows.Forms.DateTimePicker dtpEnd;
        private System.Windows.Forms.Label lblJobEnd;
        private System.Windows.Forms.Label lblJobStart;
        private System.Windows.Forms.Label lblJobTitle;
        private System.Windows.Forms.ComboBox cbJobTitle;
        private System.Windows.Forms.Label lblJobDepartment;
        private System.Windows.Forms.ComboBox cbJobDepartment;
        private System.Windows.Forms.SaveFileDialog dlgSave;
        private System.Windows.Forms.OpenFileDialog dlgEdit;
        private System.Windows.Forms.CheckBox cbContinuing;
        private System.Windows.Forms.StatusStrip ssStatusStrip;
        private System.Windows.Forms.ToolStripStatusLabel sslStatus;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.ErrorProvider errorProvider;
        private System.Windows.Forms.Timer tmrSaved;
        private System.Windows.Forms.HelpProvider helpProvider;
    }
}

