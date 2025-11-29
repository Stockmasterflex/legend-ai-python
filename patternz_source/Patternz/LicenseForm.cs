using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class LicenseForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	internal virtual Button DoneButton
	{
		[CompilerGenerated]
		get
		{
			return _DoneButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DoneButton_Click;
			Button val = _DoneButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DoneButton = value;
			val = _DoneButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("ListBox1")]
	internal virtual ListBox ListBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RadioButton1")]
	internal virtual RadioButton RadioButton1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("RadioButton2")]
	internal virtual RadioButton RadioButton2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public LicenseForm()
	{
		((Form)this).Load += LicenseForm_Load;
		InitializeComponent();
	}

	[DebuggerNonUserCode]
	protected override void Dispose(bool disposing)
	{
		try
		{
			if (disposing && components != null)
			{
				components.Dispose();
			}
		}
		finally
		{
			((Form)this).Dispose(disposing);
		}
	}

	[DebuggerStepThrough]
	private void InitializeComponent()
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_000b: Expected O, but got Unknown
		//IL_000c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_0017: Unknown result type (might be due to invalid IL or missing references)
		//IL_0021: Expected O, but got Unknown
		//IL_0022: Unknown result type (might be due to invalid IL or missing references)
		//IL_002c: Expected O, but got Unknown
		DoneButton = new Button();
		ListBox1 = new ListBox();
		RadioButton1 = new RadioButton();
		RadioButton2 = new RadioButton();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(350, 362);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(75, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)ListBox1).Anchor = (AnchorStyles)15;
		((ListControl)ListBox1).FormattingEnabled = true;
		((Control)ListBox1).Location = new Point(2, 12);
		((Control)ListBox1).Name = "ListBox1";
		((Control)ListBox1).Size = new Size(432, 329);
		((Control)ListBox1).TabIndex = 1;
		((Control)RadioButton1).Anchor = (AnchorStyles)6;
		((ButtonBase)RadioButton1).AutoSize = true;
		((Control)RadioButton1).Location = new Point(12, 345);
		((Control)RadioButton1).Name = "RadioButton1";
		((Control)RadioButton1).Size = new Size(272, 17);
		((Control)RadioButton1).TabIndex = 2;
		((ButtonBase)RadioButton1).Text = "I &agree to abide by the End User License Agreement";
		((ButtonBase)RadioButton1).UseVisualStyleBackColor = true;
		((Control)RadioButton2).Anchor = (AnchorStyles)6;
		((ButtonBase)RadioButton2).AutoSize = true;
		RadioButton2.Checked = true;
		((Control)RadioButton2).Location = new Point(12, 368);
		((Control)RadioButton2).Name = "RadioButton2";
		((Control)RadioButton2).Size = new Size(323, 17);
		((Control)RadioButton2).TabIndex = 3;
		RadioButton2.TabStop = true;
		((ButtonBase)RadioButton2).Text = "I do &NOT AGREE to abide by the End User License Agreement";
		((ButtonBase)RadioButton2).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(437, 397);
		((Control)this).Controls.Add((Control)(object)RadioButton2);
		((Control)this).Controls.Add((Control)(object)RadioButton1);
		((Control)this).Controls.Add((Control)(object)ListBox1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "LicenseForm";
		((Form)this).StartPosition = (FormStartPosition)1;
		((Form)this).Text = "License Form";
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		GlobalForm.SignedLicense = Conversions.ToBoolean(Interaction.IIf(RadioButton2.Checked, (object)false, (object)true));
		((Form)this).Close();
	}

	private void LicenseForm_Load(object sender, EventArgs e)
	{
		RadioButton2.Checked = true;
		ListBox1.Items.Add((object)"Patternz software is shareware, provided free of charge without any usage");
		ListBox1.Items.Add((object)"fees. Please back up your computer system before running this program.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"This SOFTWARE Is for educational and entertainment only. You and you alone are");
		ListBox1.Items.Add((object)"responsible for your investment decisions. Do not depend on the information");
		ListBox1.Items.Add((object)"provided by Patternz to be accurate or correct. Read this paragraph again.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"IMPORTANT-READ CAREFULLY: This End-User License Agreement ('EULA') is");
		ListBox1.Items.Add((object)"a legal agreement between you and the manufacturer ('Manufacturer') of the");
		ListBox1.Items.Add((object)"Patternz software. The software ('SOFTWARE') includes the Patternz");
		ListBox1.Items.Add((object)"computer software, and may include associated media, printed materials,");
		ListBox1.Items.Add((object)"online, or electronic documentation, and Internet based services.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"END-USER LICENSE AGREEMENT");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"YOU AGREE TO BE BOUND BY THE TERMS OF THIS EULA BY USING THE");
		ListBox1.Items.Add((object)"SOFTWARE. IF YOU DO NOT AGREE TO THE TERMS OF THIS EULA, YOU");
		ListBox1.Items.Add((object)"MAY NOT USE THE SOFTWARE.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"SOFTWARE PRODUCT LICENSE");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"1. GRANT OF LICENSE.");
		ListBox1.Items.Add((object)"Manufacturer grants you the following rights provided that you comply with all");
		ListBox1.Items.Add((object)"terms and conditions of this EULA:");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"1.1 Installation and use. You may install, use, access, display and run as many");
		ListBox1.Items.Add((object)"copies of the SOFTWARE as you wish.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"1.2 You may make as many back-up copies of the SOFTWARE as you wish.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"2. RESERVATION OF RIGHTS AND OWNERSHIP.");
		ListBox1.Items.Add((object)"Manufacturer and its suppliers reserve all rights not expressly granted to you in");
		ListBox1.Items.Add((object)"this EULA. The SOFTWARE is protected by copyright and other intellectual");
		ListBox1.Items.Add((object)"property laws and treaties. Manufacturer and its suppliers own the title,");
		ListBox1.Items.Add((object)"copyright, and other intellectual property rights in the SOFTWARE. The");
		ListBox1.Items.Add((object)"SOFTWARE is licensed, not sold.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"3. NO RENTAL/COMMERCIAL HOSTING. You may not rent, lease, lend or");
		ListBox1.Items.Add((object)"provide commercial hosting services with the SOFTWARE to others.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"4. TRADEMARKS. This EULA does not grant you any rights in connection with");
		ListBox1.Items.Add((object)"any trademarks or service marks of Manufacturer or its suppliers.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"5. PRODUCT SUPPORT. Support for the SOFTWARE is not provided.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"6. ADDITIONAL SOFTWARE/SERVICES. This EULA applies to updates,");
		ListBox1.Items.Add((object)"supplements, add-on components, product support services, documentation or");
		ListBox1.Items.Add((object)"Internet-based services components, of the SOFTWARE that you may obtain.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"7. TERMINATION. Without prejudice to any other rights, Manufacturer may");
		ListBox1.Items.Add((object)"terminate this EULA if you fail to comply with the terms and conditions of");
		ListBox1.Items.Add((object)"this EULA.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"8. DISCLAIMER OF WARRANTIES.");
		ListBox1.Items.Add((object)"You understand and agree that use of the software is at your own risk.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"This SOFTWARE is provided on an 'as is' basis, without warranty of any kind,");
		ListBox1.Items.Add((object)"either expressed or implied, including but not limited to the warranties of");
		ListBox1.Items.Add((object)"merchantability, fitness for a particular purpose, and ");
		ListBox1.Items.Add((object)"non-infringement, with respect to the software or documentation. The");
		ListBox1.Items.Add((object)"entire risk with respect to the quality and performance of the SOFTWARE is");
		ListBox1.Items.Add((object)"born by you. Should the SOFTWARE prove defective, you alone assume the");
		ListBox1.Items.Add((object)"entire cost of any service, repair, or loss of investment. Some states do not allow");
		ListBox1.Items.Add((object)"exclusions of an implied warranty, so this disclaimer may not apply to you and you may");
		ListBox1.Items.Add((object)"have other legal rights that vary from state to state or by jurisdiction.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"Any material downloaded or otherwise obtained through the use of this SOFTWARE");
		ListBox1.Items.Add((object)"is accessed at your own discretion and risk, and you will be solely responsible");
		ListBox1.Items.Add((object)"for and hereby waive any and all claims and causes of action with respect to any");
		ListBox1.Items.Add((object)"damage to your computer system, internet access, download device, or data that");
		ListBox1.Items.Add((object)"results from the download of any such material.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"Under no circumstances and under no legal theory, tort, contract, or otherwise,");
		ListBox1.Items.Add((object)"shall the Manufacturer of this SOFTWARE, its respective licensors, suppliers,");
		ListBox1.Items.Add((object)"nor resellers be liable to you or any other person or entity for any indirect,");
		ListBox1.Items.Add((object)"special, incidental, exemplary, or consequential damages of any character");
		ListBox1.Items.Add((object)"including, but not limited to, damages for legal fees, damages for use or");
		ListBox1.Items.Add((object)"performance of the SOFTWARE, nor for damages for loss of profits, capital,");
		ListBox1.Items.Add((object)"goodwill, work stoppage, computer failure or malfunction, nor any and all other");
		ListBox1.Items.Add((object)"commercial damages or losses. The Manufacturer shall have no liability for any");
		ListBox1.Items.Add((object)"data stored or processed with this software, including the costs of recovering");
		ListBox1.Items.Add((object)"such data.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"In no event will the total liability of the Manufacturer, and their respective");
		ListBox1.Items.Add((object)"licensors, if any, exceed the end user fee paid to the Manufacturer for a");
		ListBox1.Items.Add((object)"license to use the software, even if the Manufacturer shall have been informed");
		ListBox1.Items.Add((object)"of the possibility of such damages, or for any claim by any other party.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"9. VENUE.");
		ListBox1.Items.Add((object)"Any court action brought against the Manufacturer by you or on your behalf");
		ListBox1.Items.Add((object)"shall be exclusively venued in the State of Texas, Tarrant County, and shall be");
		ListBox1.Items.Add((object)"governed by the laws of the State of Texas. You hereby submit to personal jurisdiction");
		ListBox1.Items.Add((object)"within the State of Texas.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"Any advice or strategies contained herein and in the documentation may not");
		ListBox1.Items.Add((object)"be suitable for your situation. You should consult with a professional where");
		ListBox1.Items.Add((object)"appropriate.");
		ListBox1.Items.Add((object)"");
		ListBox1.Items.Add((object)"Updated 1/2020");
	}
}
