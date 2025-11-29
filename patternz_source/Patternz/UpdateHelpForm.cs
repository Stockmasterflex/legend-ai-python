using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class UpdateHelpForm : Form
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

	[field: AccessedThroughProperty("Label9")]
	internal virtual Label Label9
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

	[field: AccessedThroughProperty("Label7")]
	internal virtual Label Label7
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

	[field: AccessedThroughProperty("Label5")]
	internal virtual Label Label5
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

	[field: AccessedThroughProperty("Label2")]
	internal virtual Label Label2
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

	[field: AccessedThroughProperty("Label10")]
	internal virtual Label Label10
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

	[field: AccessedThroughProperty("Label4")]
	internal virtual Label Label4
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

	public UpdateHelpForm()
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
		//IL_0268: Unknown result type (might be due to invalid IL or missing references)
		//IL_0272: Expected O, but got Unknown
		ComponentResourceManager componentResourceManager = new ComponentResourceManager(typeof(UpdateHelpForm));
		DoneButton = new Button();
		Label9 = new Label();
		Label8 = new Label();
		Label7 = new Label();
		PictureBox1 = new PictureBox();
		Label5 = new Label();
		Label3 = new Label();
		Label2 = new Label();
		Label1 = new Label();
		Label10 = new Label();
		Label12 = new Label();
		Label4 = new Label();
		Label6 = new Label();
		((ISupportInitialize)PictureBox1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)DoneButton).Anchor = (AnchorStyles)0;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(818, 491);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)Label9).Location = new Point(413, 376);
		((Control)Label9).Name = "Label9";
		((Control)Label9).Size = new Size(459, 60);
		((Control)Label9).TabIndex = 8;
		Label9.Text = componentResourceManager.GetString("Label9.Text");
		((Control)Label8).Location = new Point(413, 343);
		((Control)Label8).Name = "Label8";
		((Control)Label8).Size = new Size(458, 19);
		((Control)Label8).TabIndex = 7;
		Label8.Text = "6. For historical quotes only, enter the start and end dates of the symbols you'd like to download.";
		((Control)Label7).Location = new Point(413, 297);
		((Control)Label7).Name = "Label7";
		((Control)Label7).Size = new Size(458, 33);
		((Control)Label7).TabIndex = 6;
		Label7.Text = "5. For historical quotes only, when adding new symbols to the list shown in 1, add each symbol separated only by a space. The \"Get historical quotes\" radio button must be selected first.";
		PictureBox1.BorderStyle = (BorderStyle)2;
		PictureBox1.Image = (Image)componentResourceManager.GetObject("PictureBox1.Image");
		PictureBox1.InitialImage = null;
		((Control)PictureBox1).Location = new Point(3, 4);
		((Control)PictureBox1).Name = "PictureBox1";
		((Control)PictureBox1).Size = new Size(404, 510);
		PictureBox1.SizeMode = (PictureBoxSizeMode)4;
		PictureBox1.TabIndex = 25;
		PictureBox1.TabStop = false;
		((Control)Label5).Location = new Point(413, 150);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(462, 34);
		((Control)Label5).TabIndex = 3;
		Label5.Text = "2. \"Start from last update\" updates each quote file to bring the information current. \"Get historical quotes\" replaces existing files with new quote information using the dates specified in 6.";
		((Control)Label3).Location = new Point(413, 78);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(458, 60);
		((Control)Label3).TabIndex = 2;
		Label3.Text = componentResourceManager.GetString("Label3.Text");
		((Control)Label2).Location = new Point(413, 12);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(458, 48);
		((Control)Label2).TabIndex = 1;
		Label2.Text = componentResourceManager.GetString("Label2.Text");
		((Control)Label1).Location = new Point(297, -35);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(341, 10);
		((Control)Label1).TabIndex = 20;
		Label1.Text = "Use this form to tell Patternz how to read your stock files. ";
		((Control)Label10).Location = new Point(413, 500);
		((Control)Label10).Name = "Label10";
		((Control)Label10).Size = new Size(192, 15);
		((Control)Label10).TabIndex = 10;
		Label10.Text = "9. Error messages appear here.";
		((Control)Label12).Location = new Point(413, 251);
		((Control)Label12).Name = "Label12";
		((Control)Label12).Size = new Size(458, 33);
		((Control)Label12).TabIndex = 5;
		Label12.Text = "4. Some quote providers require a token or key code and/or the selection of a database. Enter that information here. It will be encrypted and stored.";
		((Control)Label4).Location = new Point(413, 193);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(462, 48);
		((Control)Label4).TabIndex = 4;
		Label4.Text = componentResourceManager.GetString("Label4.Text");
		((Control)Label6).Location = new Point(413, 451);
		((Control)Label6).Name = "Label6";
		((Control)Label6).Size = new Size(459, 37);
		((Control)Label6).TabIndex = 9;
		Label6.Text = "8. This is the retry list box. If a quote provider returns an error, the symbol will be put here. Switch quote providers (3) and click \"Retry\" (3) to update the symbols listed in the retry list box. ";
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(883, 529);
		((Control)this).Controls.Add((Control)(object)Label6);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)Label12);
		((Control)this).Controls.Add((Control)(object)Label10);
		((Control)this).Controls.Add((Control)(object)Label9);
		((Control)this).Controls.Add((Control)(object)Label8);
		((Control)this).Controls.Add((Control)(object)Label7);
		((Control)this).Controls.Add((Control)(object)PictureBox1);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "UpdateHelpForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Update Help Form";
		((ISupportInitialize)PictureBox1).EndInit();
		((Control)this).ResumeLayout(false);
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}
}
