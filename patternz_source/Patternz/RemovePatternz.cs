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
public class RemovePatternz : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DeleteButton")]
	private Button _DeleteButton;

	private string RegString;

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
			EventHandler eventHandler = CancelButton_Click;
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

	internal virtual Button DeleteButton
	{
		[CompilerGenerated]
		get
		{
			return _DeleteButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = DeleteButton_Click;
			Button val = _DeleteButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_DeleteButton = value;
			val = _DeleteButton;
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

	public RemovePatternz()
	{
		RegString = "Software\\PatternzSoftware";
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
		//IL_0038: Unknown result type (might be due to invalid IL or missing references)
		//IL_0042: Expected O, but got Unknown
		//IL_0043: Unknown result type (might be due to invalid IL or missing references)
		//IL_004d: Expected O, but got Unknown
		//IL_01ff: Unknown result type (might be due to invalid IL or missing references)
		//IL_0209: Expected O, but got Unknown
		//IL_0273: Unknown result type (might be due to invalid IL or missing references)
		//IL_027d: Expected O, but got Unknown
		//IL_02e7: Unknown result type (might be due to invalid IL or missing references)
		//IL_02f1: Expected O, but got Unknown
		DoneButton = new Button();
		DeleteButton = new Button();
		Label1 = new Label();
		Label2 = new Label();
		Label3 = new Label();
		Label4 = new Label();
		Label5 = new Label();
		((Control)this).SuspendLayout();
		((ButtonBase)DoneButton).BackColor = SystemColors.Control;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(230, 199);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(75, 23);
		((Control)DoneButton).TabIndex = 0;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = false;
		((Control)DeleteButton).Location = new Point(15, 199);
		((Control)DeleteButton).Name = "DeleteButton";
		((Control)DeleteButton).Size = new Size(157, 23);
		((Control)DeleteButton).TabIndex = 1;
		((ButtonBase)DeleteButton).Text = "Delete Patternz from &Registry";
		((ButtonBase)DeleteButton).UseVisualStyleBackColor = true;
		((Control)Label1).Location = new Point(47, 131);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(230, 45);
		((Control)Label1).TabIndex = 6;
		Label1.Text = "Use Add/Remove (Uninstall a program option in control panel) to remove Patternz from your computer.";
		((Control)Label2).Location = new Point(47, 69);
		((Control)Label2).Name = "Label2";
		((Control)Label2).Size = new Size(233, 32);
		((Control)Label2).TabIndex = 4;
		Label2.Text = "Click \"Delete Patternz from Registry\" (below) to remove Patternz's registration information.";
		((Control)Label3).Font = new Font("Microsoft Sans Serif", 10f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label3).Location = new Point(12, 9);
		((Control)Label3).Name = "Label3";
		((Control)Label3).Size = new Size(293, 19);
		((Control)Label3).TabIndex = 2;
		Label3.Text = "Removing Patternz from your computer";
		((Control)Label4).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label4).Location = new Point(12, 49);
		((Control)Label4).Name = "Label4";
		((Control)Label4).Size = new Size(268, 20);
		((Control)Label4).TabIndex = 3;
		Label4.Text = "Step 1";
		((Control)Label5).Font = new Font("Microsoft Sans Serif", 8.25f, (FontStyle)1, (GraphicsUnit)3, (byte)0);
		((Control)Label5).Location = new Point(12, 111);
		((Control)Label5).Name = "Label5";
		((Control)Label5).Size = new Size(268, 20);
		((Control)Label5).TabIndex = 5;
		Label5.Text = "Step 2";
		((Form)this).AcceptButton = (IButtonControl)(object)DoneButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(318, 233);
		((Control)this).Controls.Add((Control)(object)Label5);
		((Control)this).Controls.Add((Control)(object)Label4);
		((Control)this).Controls.Add((Control)(object)Label3);
		((Control)this).Controls.Add((Control)(object)Label2);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)DeleteButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Form)this).FormBorderStyle = (FormBorderStyle)1;
		((Control)this).Name = "RemovePatternz";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Remove Patternz Form";
		((Control)this).ResumeLayout(false);
	}

	private void CancelButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void DeleteButton_Click(object sender, EventArgs e)
	{
		//IL_0012: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Invalid comparison between Unknown and I4
		//IL_0055: Unknown result type (might be due to invalid IL or missing references)
		//IL_0081: Unknown result type (might be due to invalid IL or missing references)
		//IL_0039: Unknown result type (might be due to invalid IL or missing references)
		if ((int)MessageBox.Show("Warning: This will remove Patternz's information from the registry. Did you want to delete the information?", "RemovePatternz: DeleteButton_Click", (MessageBoxButtons)4, (MessageBoxIcon)32, (MessageBoxDefaultButton)256) == 6)
		{
			try
			{
				((ServerComputer)MyProject.Computer).Registry.CurrentUser.DeleteSubKeyTree(RegString);
				MessageBox.Show("Information successfully deleted.");
			}
			catch (ArgumentException ex)
			{
				ProjectData.SetProjectError((Exception)ex);
				ArgumentException ex2 = ex;
				MessageBox.Show("The information has already been deleted.", "RemovePatternz: DeleteButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
				ProjectData.ClearProjectError();
			}
			catch (Exception ex3)
			{
				ProjectData.SetProjectError(ex3);
				Exception ex4 = ex3;
				MessageBox.Show("The following error occurred when trying to remove the registry information: " + ex4.Message, "RemovePatternz: DeleteButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)16);
				ProjectData.ClearProjectError();
			}
			GlobalForm.RemovePatternzFlag = true;
		}
	}
}
