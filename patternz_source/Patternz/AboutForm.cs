using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class AboutForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PictureBox1")]
	private PictureBox _PictureBox1;

	[CompilerGenerated]
	[AccessedThroughProperty("PictureBox2")]
	private PictureBox _PictureBox2;

	[CompilerGenerated]
	[AccessedThroughProperty("LinkLabel1")]
	private LinkLabel _LinkLabel1;

	[CompilerGenerated]
	[AccessedThroughProperty("DonateButton")]
	private Button _DonateButton;

	[field: AccessedThroughProperty("Label6")]
	internal virtual Label Label6
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

	[field: AccessedThroughProperty("Label1")]
	internal virtual Label Label1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual PictureBox PictureBox1
	{
		[CompilerGenerated]
		get
		{
			return _PictureBox1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PictureBox1_Click;
			EventHandler eventHandler2 = PictureBox1_MouseHover;
			EventHandler eventHandler3 = PictureBox1_MouseLeave;
			PictureBox val = _PictureBox1;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
				((Control)val).MouseHover -= eventHandler2;
				((Control)val).MouseLeave -= eventHandler3;
			}
			_PictureBox1 = value;
			val = _PictureBox1;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
				((Control)val).MouseHover += eventHandler2;
				((Control)val).MouseLeave += eventHandler3;
			}
		}
	}

	internal virtual PictureBox PictureBox2
	{
		[CompilerGenerated]
		get
		{
			return _PictureBox2;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PictureBox1_MouseHover;
			EventHandler eventHandler2 = PictureBox1_MouseLeave;
			EventHandler eventHandler3 = PictureBox2_Click;
			PictureBox val = _PictureBox2;
			if (val != null)
			{
				((Control)val).MouseHover -= eventHandler;
				((Control)val).MouseLeave -= eventHandler2;
				((Control)val).Click -= eventHandler3;
			}
			_PictureBox2 = value;
			val = _PictureBox2;
			if (val != null)
			{
				((Control)val).MouseHover += eventHandler;
				((Control)val).MouseLeave += eventHandler2;
				((Control)val).Click += eventHandler3;
			}
		}
	}

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual LinkLabel LinkLabel1
	{
		[CompilerGenerated]
		get
		{
			return _LinkLabel1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			//IL_0007: Unknown result type (might be due to invalid IL or missing references)
			//IL_000d: Expected O, but got Unknown
			LinkLabelLinkClickedEventHandler val = new LinkLabelLinkClickedEventHandler(LinkLabel1_LinkClicked);
			LinkLabel val2 = _LinkLabel1;
			if (val2 != null)
			{
				val2.LinkClicked -= val;
			}
			_LinkLabel1 = value;
			val2 = _LinkLabel1;
			if (val2 != null)
			{
				val2.LinkClicked += val;
			}
		}
	}

	internal virtual Button DonateButton
	{
		[CompilerGenerated]
		get
		{
			return _DonateButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DonateButton_Click;
			Button val = _DonateButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DonateButton = value;
			val = _DonateButton;
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

	public AboutForm()
	{
		((Form)this).Load += AboutForm_Load;
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
		//IL_01b6: Unknown result type (might be due to invalid IL or missing references)
		//IL_01c0: Expected O, but got Unknown
		//IL_0231: Unknown result type (might be due to invalid IL or missing references)
		//IL_023b: Expected O, but got Unknown
		//IL_0388: Unknown result type (might be due to invalid IL or missing references)
		//IL_0392: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(AboutForm));
		Label6 = new Label();
		DoneButton = new Button();
		Label1 = new Label();
		PictureBox1 = new PictureBox();
		PictureBox2 = new PictureBox();
		Label2 = new Label();
		LinkLabel1 = new LinkLabel();
		DonateButton = new Button();
		Label3 = new Label();
		((ISupportInitialize)PictureBox1).BeginInit();
		((ISupportInitialize)PictureBox2).BeginInit();
		((Control)this).SuspendLayout();
		((Control)Label6).Location = new Point(15, 102);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(289, 43);
		((Control)Label6).TabIndex = 21;
		Label6.Text = "This program is for personal use only. It was written by and provided free by Thomas Bulkowski. For more information, visit";
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(226, 397);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(75, 23);
		((Control)DoneButton).TabIndex = 20;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label1).Location = new Point(15, 158);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(292, 58);
		((Control)Label1).TabIndex = 22;
		PictureBox1.Image = (Image)componentResourceManager.GetObject("PictureBox1.Image");
		((Control)PictureBox1).Location = new Point(11, 310);
		((Control)PictureBox1).Name = "PictureBox1";
		((Control)PictureBox1).Size = new Size(76, 110);
		PictureBox1.SizeMode = (PictureBoxSizeMode)2;
		PictureBox1.TabIndex = 23;
		PictureBox1.TabStop = false;
		PictureBox2.Image = (Image)componentResourceManager.GetObject("PictureBox2.Image");
		((Control)PictureBox2).Location = new Point(111, 310);
		((Control)PictureBox2).Name = "PictureBox2";
		((Control)PictureBox2).Size = new Size(78, 110);
		PictureBox2.SizeMode = (PictureBoxSizeMode)2;
		PictureBox2.TabIndex = 24;
		PictureBox2.TabStop = false;
		((Control)Label2).Location = new Point(9, 235);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(295, 55);
		((Control)Label2).TabIndex = 25;
		Label2.Text = "For more information on chart patterns, buy a copy of my book, \"Encyclopedia of Chart Patterns, Second Edition\" or for candlesticks, buy, \"Encyclopedia of Candlestick Charts.\" Click the images below.";
		((Label)LinkLabel1).AutoSize = true;
		((Control)LinkLabel1).Location = new Point(40, 128);
		((Control)LinkLabel1).Name = "LinkLabel1";
		((Control)LinkLabel1).Size = new Size(137, 13);
		((Control)LinkLabel1).TabIndex = 26;
		LinkLabel1.TabStop = true;
		LinkLabel1.Text = "http://ThePatternSite.com/";
		DonateButton.DialogResult = (DialogResult)2;
		((Control)DonateButton).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)DonateButton).ForeColor = Color.Red;
		((Control)DonateButton).Location = new Point(100, 55);
		((Control)DonateButton).Name = "DonateButton";
		((Control)DonateButton).Size = new Size(106, 23);
		((Control)DonateButton).TabIndex = 27;
		((ButtonBase)DonateButton).Text = "Paypal: &Donate";
		((ButtonBase)DonateButton).UseVisualStyleBackColor = true;
		((Control)Label3).Location = new Point(9, 9);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(289, 33);
		((Control)Label3).TabIndex = 28;
		Label3.Text = "Want to support development of this program? Click the Donate button below to take you to paypal.";
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(316, 432);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)DonateButton);
		((Control)this).Controls.Add((Control)(object)LinkLabel1);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)PictureBox2);
		((Control)this).Controls.Add((Control)(object)PictureBox1);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Name = "AboutForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "About Form";
		((ISupportInitialize)PictureBox1).EndInit();
		((ISupportInitialize)PictureBox2).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void AboutForm_Load(object sender, EventArgs e)
	{
		Label1.Text = "Version: " + ((ApplicationBase)MyProject.Application).Info.Version.ToString() + ". \r\n\r\nCopyright (c) 2016-2024 by Thomas Bulkowski and ThePatternSite.com. All rights reserved.";
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void LinkLabel1_LinkClicked(object sender, LinkLabelLinkClickedEventArgs e)
	{
		LinkLabel1.LinkVisited = true;
		Process.Start("http://ThePatternSite.com/");
	}

	private void PictureBox1_Click(object sender, EventArgs e)
	{
		Process.Start("http://www.amazon.com/gp/product/0471668265/ref=as_li_qf_sp_asin_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0471668265&linkCode=as2&tag=bulkowskschar-20");
	}

	private void PictureBox1_MouseHover(object sender, EventArgs e)
	{
		((Control)this).Cursor = Cursors.Hand;
	}

	private void PictureBox1_MouseLeave(object sender, EventArgs e)
	{
		((Control)this).Cursor = Cursors.Default;
	}

	private void PictureBox2_Click(object sender, EventArgs e)
	{
		Process.Start("http://www.amazon.com/gp/product/0470182016/ref=as_li_qf_sp_asin_tl?ie=UTF8&camp=1789&creative=9325&creativeASIN=0470182016&linkCode=as2&tag=bulkowskschar-20");
	}

	private void DonateButton_Click(object sender, EventArgs e)
	{
		Process.Start("https://www.paypal.com/donate/?token=1elxrjqhirJ-TrlEZuzwUkB06UbUtSFivac0hfa6vcnGUhR8kKzP-q2VZYptzfOueGgyom&country.x=US&locale.x=US");
	}
}
