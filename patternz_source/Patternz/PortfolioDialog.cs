using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.Runtime.CompilerServices;
using System.Windows.Forms;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class PortfolioDialog : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("CancelButton1")]
	private Button _CancelButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("OKButton")]
	private Button _OKButton;

	internal virtual Button CancelButton1
	{
		[CompilerGenerated]
		get
		{
			return _CancelButton1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = CancelButton_Click;
			Button val = _CancelButton1;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_CancelButton1 = value;
			val = _CancelButton1;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
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

	[field: AccessedThroughProperty("PortfolioDataGridView")]
	internal virtual DataGridView PortfolioDataGridView
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("PortfolioColumn")]
	internal virtual DataGridViewTextBoxColumn PortfolioColumn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("PathColumn")]
	internal virtual DataGridViewTextBoxColumn PathColumn
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	public PortfolioDialog()
	{
		((Form)this).Load += PortfolioDialog_Load;
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
		CancelButton1 = new Button();
		OKButton = new Button();
		PortfolioDataGridView = new DataGridView();
		PortfolioColumn = new DataGridViewTextBoxColumn();
		PathColumn = new DataGridViewTextBoxColumn();
		((ISupportInitialize)PortfolioDataGridView).BeginInit();
		((Control)this).SuspendLayout();
		((Control)CancelButton1).Anchor = (AnchorStyles)10;
		CancelButton1.DialogResult = (DialogResult)2;
		((Control)CancelButton1).Location = new Point(145, 238);
		((Control)CancelButton1).Name = "CancelButton1";
		((Control)CancelButton1).Size = new Size(75, 23);
		((Control)CancelButton1).TabIndex = 2;
		((ButtonBase)CancelButton1).Text = "&Cancel";
		((ButtonBase)CancelButton1).UseVisualStyleBackColor = true;
		((Control)OKButton).Anchor = (AnchorStyles)10;
		OKButton.DialogResult = (DialogResult)1;
		((Control)OKButton).Location = new Point(64, 238);
		((Control)OKButton).Name = "OKButton";
		((Control)OKButton).Size = new Size(75, 23);
		((Control)OKButton).TabIndex = 1;
		((ButtonBase)OKButton).Text = "&OK";
		((ButtonBase)OKButton).UseVisualStyleBackColor = true;
		PortfolioDataGridView.AllowUserToAddRows = false;
		PortfolioDataGridView.AllowUserToDeleteRows = false;
		((Control)PortfolioDataGridView).Anchor = (AnchorStyles)15;
		((Control)PortfolioDataGridView).CausesValidation = false;
		PortfolioDataGridView.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		PortfolioDataGridView.Columns.AddRange((DataGridViewColumn[])(object)new DataGridViewColumn[2]
		{
			(DataGridViewColumn)PortfolioColumn,
			(DataGridViewColumn)PathColumn
		});
		PortfolioDataGridView.EditMode = (DataGridViewEditMode)4;
		((Control)PortfolioDataGridView).Location = new Point(12, 12);
		PortfolioDataGridView.MultiSelect = false;
		((Control)PortfolioDataGridView).Name = "PortfolioDataGridView";
		PortfolioDataGridView.ReadOnly = true;
		PortfolioDataGridView.RowHeadersWidth = 4;
		PortfolioDataGridView.RowHeadersWidthSizeMode = (DataGridViewRowHeadersWidthSizeMode)1;
		PortfolioDataGridView.SelectionMode = (DataGridViewSelectionMode)1;
		PortfolioDataGridView.ShowCellErrors = false;
		PortfolioDataGridView.ShowCellToolTips = false;
		PortfolioDataGridView.ShowEditingIcon = false;
		PortfolioDataGridView.ShowRowErrors = false;
		((Control)PortfolioDataGridView).Size = new Size(255, 220);
		((Control)PortfolioDataGridView).TabIndex = 0;
		((DataGridViewColumn)PortfolioColumn).AutoSizeMode = (DataGridViewAutoSizeColumnMode)16;
		((DataGridViewColumn)PortfolioColumn).HeaderText = "                           Select a Portfolio";
		((DataGridViewColumn)PortfolioColumn).Name = "PortfolioColumn";
		((DataGridViewColumn)PortfolioColumn).ReadOnly = true;
		((DataGridViewColumn)PathColumn).HeaderText = "Path";
		((DataGridViewColumn)PathColumn).Name = "PathColumn";
		((DataGridViewColumn)PathColumn).ReadOnly = true;
		((DataGridViewColumn)PathColumn).Visible = false;
		((Form)this).AcceptButton = (IButtonControl)(object)OKButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).ClientSize = new Size(279, 273);
		((Control)this).Controls.Add((Control)(object)PortfolioDataGridView);
		((Control)this).Controls.Add((Control)(object)CancelButton1);
		((Control)this).Controls.Add((Control)(object)OKButton);
		((Control)this).Name = "PortfolioDialog";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Choose A Portfolio";
		((ISupportInitialize)PortfolioDataGridView).EndInit();
		((Control)this).ResumeLayout(false);
	}

	private void CancelButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.CustomResult = (DialogResult)2;
		((Form)this).Close();
	}

	private void OKButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		GlobalForm.CustomResult = (DialogResult)1;
		GlobalForm.PDSelectionPath = PortfolioDataGridView.SelectedCells[1].Value.ToString();
		((Form)this).Close();
	}

	private void PortfolioDialog_Load(object sender, EventArgs e)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_003e: Unknown result type (might be due to invalid IL or missing references)
		//IL_016d: Unknown result type (might be due to invalid IL or missing references)
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)PortfolioDataGridView, "Select the portfolio you wish to use.");
		val.SetToolTip((Control)(object)OKButton, "Click to accept the selection.");
		val.SetToolTip((Control)(object)CancelButton1, "Click to disregard the selection.");
		PortfolioDataGridView.RowCount = 0;
		checked
		{
			if (MyProject.Forms.Mainform.PortfolioDataGridView.RowCount > 0)
			{
				int num = MyProject.Forms.Mainform.PortfolioDataGridView.RowCount - 1;
				for (int i = 0; i <= num; i++)
				{
					PortfolioDataGridView.Rows.Add();
					PortfolioDataGridView.Rows[i].Cells[0].Value = RuntimeHelpers.GetObjectValue(MyProject.Forms.Mainform.PortfolioDataGridView.Rows[i].Cells[0].Value);
					PortfolioDataGridView.Rows[i].Cells[1].Value = RuntimeHelpers.GetObjectValue(MyProject.Forms.Mainform.PortfolioDataGridView.Rows[i].Cells[1].Value);
				}
			}
			else
			{
				MessageBox.Show("There are no portfolios to show.", "PortfolioDialog_Load", (MessageBoxButtons)0, (MessageBoxIcon)64);
				CancelButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			}
		}
	}
}
