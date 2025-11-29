using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class FileFormatHelp : Form
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

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("PictureBox1")]
	internal virtual PictureBox PictureBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label9")]
	internal virtual Label Label9
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label10")]
	internal virtual Label Label10
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label11")]
	internal virtual Label Label11
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label12")]
	internal virtual Label Label12
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label13")]
	internal virtual Label Label13
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public FileFormatHelp()
	{
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
		//IL_0011: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Expected O, but got Unknown
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Expected O, but got Unknown
		//IL_0027: Unknown result type (might be due to invalid IL or missing references)
		//IL_0031: Expected O, but got Unknown
		//IL_0032: Unknown result type (might be due to invalid IL or missing references)
		//IL_003c: Expected O, but got Unknown
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0047: Expected O, but got Unknown
		//IL_0048: Unknown result type (might be due to invalid IL or missing references)
		//IL_0052: Expected O, but got Unknown
		//IL_0053: Unknown result type (might be due to invalid IL or missing references)
		//IL_005d: Expected O, but got Unknown
		//IL_005e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0068: Expected O, but got Unknown
		//IL_0069: Unknown result type (might be due to invalid IL or missing references)
		//IL_0073: Expected O, but got Unknown
		//IL_0074: Unknown result type (might be due to invalid IL or missing references)
		//IL_007e: Expected O, but got Unknown
		//IL_007f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0089: Expected O, but got Unknown
		//IL_008a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0094: Expected O, but got Unknown
		//IL_0095: Unknown result type (might be due to invalid IL or missing references)
		//IL_009f: Expected O, but got Unknown
		//IL_00a0: Unknown result type (might be due to invalid IL or missing references)
		//IL_00aa: Expected O, but got Unknown
		//IL_0324: Unknown result type (might be due to invalid IL or missing references)
		//IL_032e: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(FileFormatHelp));
		DoneButton = new Button();
		Label1 = new Label();
		Label2 = new Label();
		Label3 = new Label();
		Label4 = new Label();
		Label5 = new Label();
		PictureBox1 = new PictureBox();
		Label9 = new Label();
		Label10 = new Label();
		Label11 = new Label();
		Label12 = new Label();
		Label13 = new Label();
		Label6 = new Label();
		Label7 = new Label();
		((ISupportInitialize)PictureBox1).BeginInit();
		((Control)this).SuspendLayout();
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(827, 701);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(75, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label1).Location = new Point(559, 13);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(341, 17);
		((Control)Label1).TabIndex = 1;
		Label1.Text = "Use this form to tell Patternz how to read your stock files. ";
		((Control)Label2).Location = new Point(558, 54);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(341, 30);
		((Control)Label2).TabIndex = 2;
		Label2.Text = "1. Click the \"Browse\" button (6) to locate your quote files if they are not already shown (2).";
		((Control)Label3).Location = new Point(558, 107);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(341, 36);
		((Control)Label3).TabIndex = 3;
		Label3.Text = "2. Click a symbol file name (2) to chart it (1) and to display quote information in the grid (3). The first few lines of the file appear at 7. ";
		((Control)Label4).Location = new Point(559, 166);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(341, 48);
		((Control)Label4).TabIndex = 4;
		Label4.Text = "3. Use the information displayed in the first few lines (7) to help determine what information the files contain and the order of the quote information. ";
		((Control)Label5).Location = new Point(584, 338);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(288, 102);
		((Control)Label5).TabIndex = 5;
		Label5.Text = componentResourceManager.GetString("Label5.Text");
		PictureBox1.BorderStyle = (BorderStyle)2;
		PictureBox1.ErrorImage = null;
		PictureBox1.Image = (Image)componentResourceManager.GetObject("PictureBox1.Image");
		PictureBox1.InitialImage = null;
		((Control)PictureBox1).Location = new Point(6, -1);
		((Control)PictureBox1).Name = "PictureBox1";
		((Control)PictureBox1).Size = new Size(547, 733);
		PictureBox1.TabIndex = 6;
		PictureBox1.TabStop = false;
		((Control)Label9).Location = new Point(561, 562);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(341, 56);
		((Control)Label9).TabIndex = 10;
		Label9.Text = "6. Select a date format (8) that matches the date shown (7). If you can't find a match, type one in: d means day, M (UPPER CASE) means month, y means year.";
		((Control)Label10).Location = new Point(559, 696);
		((Control)Label10).Name = "Label10";
		((Control)Label10).Size = new Size(262, 26);
		((Control)Label10).TabIndex = 11;
		Label10.Text = "8. Click the Save button (6) to save changes.";
		((Control)Label11).Location = new Point(559, 238);
		((Control)Label11).Name = "Label11";
		((Control)Label11).Size = new Size(341, 22);
		((Control)Label11).TabIndex = 12;
		Label11.Text = "4. Check or uncheck (4) the check boxes to match what you see in 7. ";
		((Control)Label12).Location = new Point(560, 627);
		((Control)Label12).Name = "Label12";
		((Control)Label12).Size = new Size(341, 58);
		((Control)Label12).TabIndex = 13;
		Label12.Text = componentResourceManager.GetString("Label12.Text");
		((Control)Label13).Location = new Point(559, 285);
		((Control)Label13).Name = "Label13";
		((Control)Label13).Size = new Size(341, 42);
		((Control)Label13).TabIndex = 14;
		Label13.Text = "5. Fill in the text boxes (5) with the column order shown in 7.  Zero means unused.";
		((Control)Label6).Location = new Point(587, 452);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(285, 37);
		((Control)Label6).TabIndex = 15;
		Label6.Text = "Ignore both Split Factor and Dividends in 7 because there is no matching control in 4.";
		((Control)Label7).Location = new Point(561, 502);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(341, 37);
		((Control)Label7).TabIndex = 16;
		Label7.Text = "5a. Check the \"Date && Time\" box (5) if both the date and time appear in the same column in 7.";
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(913, 736);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label13);
		((Control)this).Controls.Add((Control)(object)Label12);
		((Control)this).Controls.Add((Control)(object)Label11);
		((Control)this).Controls.Add((Control)(object)Label10);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)PictureBox1);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Form)this).MaximizeBox = false;
		((Form)this).MinimizeBox = false;
		((Control)this).Name = "FileFormatHelp";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "File Format Form Help";
		((ISupportInitialize)PictureBox1).EndInit();
		((Control)this).ResumeLayout(false);
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}
}
