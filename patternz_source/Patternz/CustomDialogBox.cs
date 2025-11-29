using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class CustomDialogBox : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("YesButton")]
	private Button _YesButton;

	[CompilerGenerated]
	[AccessedThroughProperty("NoButton")]
	private Button _NoButton;

	internal virtual Button YesButton
	{
		[CompilerGenerated]
		get
		{
			return _YesButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = YesButton_Click;
			Button val = _YesButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_YesButton = value;
			val = _YesButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button NoButton
	{
		[CompilerGenerated]
		get
		{
			return _NoButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = NoButton_Click;
			Button val = _NoButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_NoButton = value;
			val = _NoButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("CheckBox1")]
	internal virtual CheckBox CheckBox1
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

	public CustomDialogBox()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosed += new FormClosedEventHandler(CustomDialogBox_FormClosed);
		((Form)this).Load += CustomDialogBox_Load;
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
		YesButton = new Button();
		NoButton = new Button();
		CheckBox1 = new CheckBox();
		Label1 = new Label();
		((Control)this).SuspendLayout();
		((Control)YesButton).Location = new Point(101, 101);
		((Control)YesButton).Name = "YesButton";
		((Control)YesButton).Size = new Size(75, 23);
		((Control)YesButton).TabIndex = 2;
		((ButtonBase)YesButton).Text = "&Yes";
		((ButtonBase)YesButton).UseVisualStyleBackColor = true;
		NoButton.DialogResult = (DialogResult)2;
		((Control)NoButton).Location = new Point(182, 101);
		((Control)NoButton).Name = "NoButton";
		((Control)NoButton).Size = new Size(75, 23);
		((Control)NoButton).TabIndex = 3;
		((ButtonBase)NoButton).Text = "&No";
		((ButtonBase)NoButton).UseVisualStyleBackColor = true;
		((ButtonBase)CheckBox1).AutoSize = true;
		((Control)CheckBox1).Location = new Point(101, 78);
		((Control)CheckBox1).Name = "CheckBox1";
		((Control)CheckBox1).Size = new Size(169, 17);
		((Control)CheckBox1).TabIndex = 1;
		((ButtonBase)CheckBox1).Text = "&Do this (yes/no) for all symbols";
		((ButtonBase)CheckBox1).UseVisualStyleBackColor = true;
		((Control)Label1).Location = new Point(3, 9);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(362, 48);
		((Control)Label1).TabIndex = 0;
		Label1.TextAlign = (ContentAlignment)32;
		((Form)this).AcceptButton = (IButtonControl)(object)YesButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)NoButton;
		((Form)this).ClientSize = new Size(365, 136);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)CheckBox1);
		((Control)this).Controls.Add((Control)(object)NoButton);
		((Control)this).Controls.Add((Control)(object)YesButton);
		((Control)this).Name = "CustomDialogBox";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "ThePatternSite.com";
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void CustomDialogBox_FormClosed(object sender, FormClosedEventArgs e)
	{
		GlobalForm.CustomCheckbox = CheckBox1.Checked;
	}

	private void CustomDialogBox_Load(object sender, EventArgs e)
	{
		Label1.Text = "The file " + GlobalForm.CurrentSymbol + ".csv already exists. Did you want me to replace it?";
		CheckBox1.Checked = GlobalForm.CustomCheckbox;
	}

	private void NoButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.CustomResult = (DialogResult)7;
		((Form)this).Close();
	}

	private void YesButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.CustomResult = (DialogResult)6;
		((Form)this).Close();
	}
}
