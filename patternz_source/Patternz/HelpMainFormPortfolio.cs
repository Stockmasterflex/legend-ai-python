using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class HelpMainFormPortfolio : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[field: AccessedThroughProperty("PictureBox1")]
	internal virtual PictureBox PictureBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

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

	[field: AccessedThroughProperty("Label3")]
	internal virtual Label Label3
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

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
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

	public HelpMainFormPortfolio()
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
		//IL_00ad: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b7: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(HelpMainFormPortfolio));
		PictureBox1 = new PictureBox();
		DoneButton = new Button();
		Label3 = new Label();
		Label1 = new Label();
		Label2 = new Label();
		Label4 = new Label();
		Label5 = new Label();
		Label7 = new Label();
		Label6 = new Label();
		((ISupportInitialize)PictureBox1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)PictureBox1).Anchor = (AnchorStyles)7;
		PictureBox1.BorderStyle = (BorderStyle)2;
		PictureBox1.Image = (Image)componentResourceManager.GetObject("PictureBox1.Image");
		((Control)PictureBox1).Location = new Point(5, 5);
		((Control)PictureBox1).Name = "PictureBox1";
		((Control)PictureBox1).Size = new Size(422, 392);
		PictureBox1.TabIndex = 3;
		PictureBox1.TabStop = false;
		((Control)DoneButton).Anchor = (AnchorStyles)15;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(723, 374);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(59, 23);
		((Control)DoneButton).TabIndex = 4;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label3).Anchor = (AnchorStyles)15;
		((Control)Label3).Location = new Point(448, 5);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(334, 34);
		((Control)Label3).TabIndex = 6;
		Label3.Text = "Portfolios allow you to easily move from folder to folder, where each folder contains different security symbols.";
		((Control)Label1).Anchor = (AnchorStyles)15;
		((Control)Label1).Location = new Point(448, 54);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(334, 20);
		((Control)Label1).TabIndex = 7;
		Label1.Text = "To use portfolios, follow these instructions.";
		((Control)Label2).Anchor = (AnchorStyles)15;
		((Control)Label2).Location = new Point(448, 74);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(334, 66);
		((Control)Label2).TabIndex = 8;
		Label2.Text = componentResourceManager.GetString("Label2.Text");
		((Control)Label4).Anchor = (AnchorStyles)15;
		((Control)Label4).Location = new Point(448, 163);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(334, 40);
		((Control)Label4).TabIndex = 10;
		Label4.Text = "To Delete a portfolio, click the one you wish to delete in 6 and click \"Delete\" (3).";
		((Control)Label5).Anchor = (AnchorStyles)15;
		((Control)Label5).Location = new Point(448, 203);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(334, 53);
		((Control)Label5).TabIndex = 9;
		Label5.Text = componentResourceManager.GetString("Label5.Text");
		((Control)Label7).Anchor = (AnchorStyles)15;
		((Control)Label7).Location = new Point(448, 283);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(334, 20);
		((Control)Label7).TabIndex = 11;
		Label7.Text = "\"Help\" (4) displays this form.";
		((Control)Label6).Anchor = (AnchorStyles)15;
		((Control)Label6).Location = new Point(448, 323);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(334, 48);
		((Control)Label6).TabIndex = 12;
		Label6.Text = "To access a portfolio, simply click the name of it listed in 6. The progam switches to that folder and displays the contents of it in 7. The path to those files appears in 8.";
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Control)this).CausesValidation = false;
		((Form)this).ClientSize = new Size(794, 409);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)PictureBox1);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "HelpMainFormPortfolio";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Help: Main Form Portfolio";
		((ISupportInitialize)PictureBox1).EndInit();
		((Control)this).ResumeLayout(false);
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}
}
