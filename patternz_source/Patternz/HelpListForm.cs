using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class HelpListForm : Form
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

	[field: AccessedThroughProperty("PictureBox1")]
	internal virtual PictureBox PictureBox1
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

	[field: AccessedThroughProperty("Label8")]
	internal virtual Label Label8
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

	public HelpListForm()
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
		//IL_0143: Unknown result type (might be due to invalid IL or missing references)
		//IL_014d: Expected O, but got Unknown
		//IL_0235: Unknown result type (might be due to invalid IL or missing references)
		//IL_023f: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(HelpListForm));
		DoneButton = new Button();
		PictureBox1 = new PictureBox();
		Label1 = new Label();
		Label2 = new Label();
		Label3 = new Label();
		Label4 = new Label();
		Label5 = new Label();
		Label6 = new Label();
		Label7 = new Label();
		Label8 = new Label();
		Label9 = new Label();
		((ISupportInitialize)PictureBox1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(943, 406);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)PictureBox1).Anchor = (AnchorStyles)10;
		PictureBox1.BorderStyle = (BorderStyle)2;
		PictureBox1.Image = (Image)componentResourceManager.GetObject("PictureBox1.Image");
		((Control)PictureBox1).Location = new Point(230, 10);
		((Control)PictureBox1).Name = "PictureBox1";
		((Control)PictureBox1).Size = new Size(776, 361);
		PictureBox1.TabIndex = 2;
		PictureBox1.TabStop = false;
		((Control)Label1).Anchor = (AnchorStyles)10;
		((Control)Label1).Location = new Point(4, 10);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(218, 53);
		((Control)Label1).TabIndex = 3;
		Label1.Text = "Use this form to find chart patterns and candlesticks and list them like that shown at B.";
		((Control)Label2).Anchor = (AnchorStyles)10;
		Label2.AutoSize = true;
		((Control)Label2).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label2).Location = new Point(54, 294);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(73, 13);
		((Control)Label2).TabIndex = 4;
		Label2.Text = "Controls (A)";
		((Control)Label3).Anchor = (AnchorStyles)10;
		((Control)Label3).Location = new Point(2, 63);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(218, 112);
		((Control)Label3).TabIndex = 5;
		Label3.Text = componentResourceManager.GetString("Label3.Text");
		((Control)Label4).Anchor = (AnchorStyles)10;
		((Control)Label4).Location = new Point(5, 175);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(219, 60);
		((Control)Label4).TabIndex = 6;
		Label4.Text = "Enter a stock symbol in the \"Symbol\" text box to search ONE stock. Otherwise, select stocks you wish to use from the Main Form.";
		((Control)Label5).Anchor = (AnchorStyles)10;
		((Control)Label5).Location = new Point(2, 246);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(218, 37);
		((Control)Label5).TabIndex = 7;
		Label5.Text = "Use the \"From\" and \"To\" dates to narrow the search to periods you wish to study.";
		((Control)Label6).Anchor = (AnchorStyles)10;
		((Control)Label6).Location = new Point(4, 392);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(279, 61);
		((Control)Label6).TabIndex = 8;
		Label6.Text = "After results appear at B, highlight rows you wish to save and click \"Clipboard.\" This copies highlighted information to the clipboard for pasting into another program.";
		((Control)Label7).Anchor = (AnchorStyles)10;
		((Control)Label7).Location = new Point(702, 395);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(235, 47);
		((Control)Label7).TabIndex = 9;
		Label7.Text = "\"Graph\" charts the highlighted grid pattern. \"Done\" returns you to the Main Form.";
		((Control)Label8).Anchor = (AnchorStyles)10;
		((Control)Label8).Location = new Point(299, 395);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(386, 47);
		((Control)Label8).TabIndex = 10;
		Label8.Text = "\"Stop\" and \"Start\" buttons end or begin a search. \"Candles\" and \"Patterns\" buttons allow access to forms where you can select candlesticks or chart patterns you wish to search.";
		((Control)Label9).Anchor = (AnchorStyles)10;
		((Control)Label9).Location = new Point(4, 328);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(217, 54);
		((Control)Label9).TabIndex = 11;
		Label9.Text = "\"Help\" shows this form and \"List All Portfolios\" scans each security in all portfolios for chart and candle patterns.";
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(1018, 451);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)PictureBox1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "HelpListForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Help List Form";
		((ISupportInitialize)PictureBox1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}
}
