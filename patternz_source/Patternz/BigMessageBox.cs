using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;

namespace Patternz;

[DesignerGenerated]
public class BigMessageBox : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("OKButton")]
	private Button _OKButton;

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button OKButton
	{
		[CompilerGenerated]
		get
		{
			return _OKButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = OKButton_Click;
			Button val = _OKButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_OKButton = value;
			val = _OKButton;
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

	[field: AccessedThroughProperty("Column1")]
	internal virtual DataGridViewTextBoxColumn Column1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column2")]
	internal virtual DataGridViewTextBoxColumn Column2
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column3")]
	internal virtual DataGridViewTextBoxColumn Column3
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column4")]
	internal virtual DataGridViewTextBoxColumn Column4
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column6")]
	internal virtual DataGridViewTextBoxColumn Column6
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("Column7")]
	internal virtual DataGridViewTextBoxColumn Column7
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public BigMessageBox()
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
		//IL_004e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0058: Expected O, but got Unknown
		//IL_0059: Unknown result type (might be due to invalid IL or missing references)
		//IL_0063: Expected O, but got Unknown
		DataGridView1 = new DataGridView();
		Column1 = new DataGridViewTextBoxColumn();
		Column2 = new DataGridViewTextBoxColumn();
		Column3 = new DataGridViewTextBoxColumn();
		Column4 = new DataGridViewTextBoxColumn();
		Column6 = new DataGridViewTextBoxColumn();
		Column7 = new DataGridViewTextBoxColumn();
		OKButton = new Button();
		Label1 = new Label();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)this).SuspendLayout();
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)15;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.Columns.AddRange((DataGridViewColumn[])(object)new DataGridViewColumn[6]
		{
			(DataGridViewColumn)Column1,
			(DataGridViewColumn)Column2,
			(DataGridViewColumn)Column3,
			(DataGridViewColumn)Column4,
			(DataGridViewColumn)Column6,
			(DataGridViewColumn)Column7
		});
		((Control)DataGridView1).Location = new Point(0, 0);
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		((Control)DataGridView1).Size = new Size(525, 230);
		((Control)DataGridView1).TabIndex = 1;
		((DataGridViewColumn)Column1).AutoSizeMode = (DataGridViewAutoSizeColumnMode)10;
		((DataGridViewColumn)Column1).HeaderText = "Date";
		((DataGridViewColumn)Column1).Name = "Column1";
		((DataGridViewColumn)Column1).ReadOnly = true;
		((DataGridViewColumn)Column1).Width = 53;
		((DataGridViewColumn)Column2).AutoSizeMode = (DataGridViewAutoSizeColumnMode)10;
		((DataGridViewColumn)Column2).HeaderText = "Bull Total";
		((DataGridViewColumn)Column2).Name = "Column2";
		((DataGridViewColumn)Column2).ReadOnly = true;
		((DataGridViewColumn)Column2).Width = 68;
		((DataGridViewColumn)Column3).AutoSizeMode = (DataGridViewAutoSizeColumnMode)10;
		((DataGridViewColumn)Column3).HeaderText = "Bear Total";
		((DataGridViewColumn)Column3).Name = "Column3";
		((DataGridViewColumn)Column3).ReadOnly = true;
		((DataGridViewColumn)Column3).Width = 73;
		((DataGridViewColumn)Column4).AutoSizeMode = (DataGridViewAutoSizeColumnMode)10;
		((DataGridViewColumn)Column4).HeaderText = "NR7s Awaiting Breakout";
		((DataGridViewColumn)Column4).Name = "Column4";
		((DataGridViewColumn)Column4).ReadOnly = true;
		((DataGridViewColumn)Column4).Width = 133;
		((DataGridViewColumn)Column6).AutoSizeMode = (DataGridViewAutoSizeColumnMode)10;
		((DataGridViewColumn)Column6).HeaderText = "CPI";
		((DataGridViewColumn)Column6).Name = "Column6";
		((DataGridViewColumn)Column6).ReadOnly = true;
		((DataGridViewColumn)Column6).Width = 47;
		((DataGridViewColumn)Column7).AutoSizeMode = (DataGridViewAutoSizeColumnMode)10;
		((DataGridViewColumn)Column7).HeaderText = "Status";
		((DataGridViewColumn)Column7).Name = "Column7";
		((DataGridViewColumn)Column7).ReadOnly = true;
		((DataGridViewColumn)Column7).Width = 60;
		((Control)OKButton).Anchor = (AnchorStyles)10;
		OKButton.DialogResult = (DialogResult)2;
		((Control)OKButton).Location = new Point(455, 236);
		((Control)OKButton).Name = "OKButton";
		((Control)OKButton).Size = new Size(60, 23);
		((Control)OKButton).TabIndex = 0;
		((ButtonBase)OKButton).Text = "&Ok";
		((ButtonBase)OKButton).UseVisualStyleBackColor = true;
		((Control)Label1).Anchor = (AnchorStyles)10;
		Label1.AutoSize = true;
		((Control)Label1).Location = new Point(181, 241);
		((Control)Label1).Name = "Label1";
		((Control)Label1).Size = new Size(183, 13);
		((Control)Label1).TabIndex = 2;
		Label1.Text = "These results can change for a week";
		((Form)this).AcceptButton = (IButtonControl)(object)OKButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)OKButton;
		((Form)this).ClientSize = new Size(527, 262);
		((Control)this).Controls.Add((Control)(object)Label1);
		((Control)this).Controls.Add((Control)(object)OKButton);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Name = "BigMessageBox";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Seven Days of Results: Any errors are on the clipboard";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void OKButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}
}
