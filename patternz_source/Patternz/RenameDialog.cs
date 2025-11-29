using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.Devices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class RenameDialog : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("OK_Button")]
	private Button _OK_Button;

	[CompilerGenerated]
	[AccessedThroughProperty("Cancel_Button")]
	private Button _Cancel_Button;

	[field: AccessedThroughProperty("TableLayoutPanel1")]
	internal virtual TableLayoutPanel TableLayoutPanel1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button OK_Button
	{
		[CompilerGenerated]
		get
		{
			return _OK_Button;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OK_Button_Click;
			Button val = _OK_Button;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_OK_Button = value;
			val = _OK_Button;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button Cancel_Button
	{
		[CompilerGenerated]
		get
		{
			return _Cancel_Button;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = Cancel_Button_Click;
			Button val = _Cancel_Button;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_Cancel_Button = value;
			val = _Cancel_Button;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("RenameTextBox")]
	internal virtual TextBox RenameTextBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public RenameDialog()
	{
		((Form)this).Load += RenameDialog_Load;
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
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0037: Expected O, but got Unknown
		//IL_0072: Unknown result type (might be due to invalid IL or missing references)
		//IL_007c: Expected O, but got Unknown
		//IL_008e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0098: Expected O, but got Unknown
		//IL_010a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0114: Expected O, but got Unknown
		TableLayoutPanel1 = new TableLayoutPanel();
		OK_Button = new Button();
		Cancel_Button = new Button();
		RenameTextBox = new TextBox();
		Label1 = new Label();
		((Control)TableLayoutPanel1).SuspendLayout();
		((Control)this).SuspendLayout();
		((Control)TableLayoutPanel1).Anchor = (AnchorStyles)10;
		TableLayoutPanel1.ColumnCount = 2;
		TableLayoutPanel1.ColumnStyles.Add(new ColumnStyle((SizeType)2, 50f));
		TableLayoutPanel1.ColumnStyles.Add(new ColumnStyle((SizeType)2, 50f));
		TableLayoutPanel1.Controls.Add((Control)(object)OK_Button, 0, 0);
		TableLayoutPanel1.Controls.Add((Control)(object)Cancel_Button, 1, 0);
		((Control)TableLayoutPanel1).Location = new Point(72, 64);
		((Control)TableLayoutPanel1).Name = "TableLayoutPanel1";
		TableLayoutPanel1.RowCount = 1;
		TableLayoutPanel1.RowStyles.Add(new RowStyle((SizeType)2, 50f));
		((Control)TableLayoutPanel1).Size = new Size(146, 29);
		((Control)TableLayoutPanel1).TabIndex = 0;
		((Control)OK_Button).Anchor = (AnchorStyles)0;
		((Control)OK_Button).Location = new Point(3, 3);
		((Control)OK_Button).Name = "OK_Button";
		((Control)OK_Button).Size = new Size(67, 23);
		((Control)OK_Button).TabIndex = 0;
		((ButtonBase)OK_Button).Text = "OK";
		((Control)Cancel_Button).Anchor = (AnchorStyles)0;
		Cancel_Button.DialogResult = (DialogResult)2;
		((Control)Cancel_Button).Location = new Point(76, 3);
		((Control)Cancel_Button).Name = "Cancel_Button";
		((Control)Cancel_Button).Size = new Size(67, 23);
		((Control)Cancel_Button).TabIndex = 1;
		((ButtonBase)Cancel_Button).Text = "Cancel";
		((Control)RenameTextBox).Anchor = (AnchorStyles)10;
		((Control)RenameTextBox).Location = new Point(121, 19);
		((Control)RenameTextBox).Name = "RenameTextBox";
		((Control)RenameTextBox).Size = new Size(100, 20);
		((Control)RenameTextBox).TabIndex = 1;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(12, 22);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(103, 13);
		((Control)Label1).TabIndex = 0;
		Label1.Text = "Rename the symbol:";
		((Form)this).AcceptButton = (IButtonControl)(object)OK_Button;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)Cancel_Button;
		((Form)this).ClientSize = new Size(230, 105);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)RenameTextBox);
		((Control)this).Controls.Add((Control)(object)TableLayoutPanel1);
		((Form)this).FormBorderStyle = (FormBorderStyle)3;
		((Form)this).MaximizeBox = false;
		((Form)this).MinimizeBox = false;
		((Control)this).Name = "RenameDialog";
		((Form)this).ShowInTaskbar = false;
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Rename Symbol Form";
		((Control)TableLayoutPanel1).ResumeLayout(false);
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void OK_Button_Click(object sender, EventArgs e)
	{
		//IL_007d: Unknown result type (might be due to invalid IL or missing references)
		//IL_004b: Unknown result type (might be due to invalid IL or missing references)
		string text = RenameTextBox.Text;
		text = text.Replace(":", "_");
		try
		{
			if (((ServerComputer)MyProject.Computer).FileSystem.FileExists(GlobalForm.OpenPath + "\\" + text))
			{
				MessageBox.Show("The file already exists.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				return;
			}
			GlobalForm.RenameSymbolString = text;
			((Form)this).DialogResult = (DialogResult)1;
			((Form)this).Close();
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show(ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
		}
	}

	private void Cancel_Button_Click(object sender, EventArgs e)
	{
		((Form)this).DialogResult = (DialogResult)2;
		((Form)this).Close();
	}

	private void RenameDialog_Load(object sender, EventArgs e)
	{
		RenameTextBox.Text = GlobalForm.RenameSymbolString;
	}
}
