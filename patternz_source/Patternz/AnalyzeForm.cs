using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.ApplicationServices;
using Microsoft.VisualBasic.CompilerServices;
using Patternz.My;

namespace Patternz;

[DesignerGenerated]
public class AnalyzeForm : Form
{
	private IContainer components;

	[CompilerGenerated]
	[AccessedThroughProperty("BrowseButton")]
	private Button _BrowseButton;

	[CompilerGenerated]
	[AccessedThroughProperty("HelpButton1")]
	private Button _HelpButton1;

	[CompilerGenerated]
	[AccessedThroughProperty("AllButton")]
	private Button _AllButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StartButton")]
	private Button _StartButton;

	[CompilerGenerated]
	[AccessedThroughProperty("DoneButton")]
	private Button _DoneButton;

	[CompilerGenerated]
	[AccessedThroughProperty("StopButton")]
	private Button _StopButton;

	[CompilerGenerated]
	[AccessedThroughProperty("ClipboardButton")]
	private Button _ClipboardButton;

	[CompilerGenerated]
	[AccessedThroughProperty("PortfolioButton")]
	private Button _PortfolioButton;

	private bool StopPressed;

	private readonly string YAHOOURLeod;

	[field: AccessedThroughProperty("ListBox1")]
	internal virtual ListBox ListBox1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button BrowseButton
	{
		[CompilerGenerated]
		get
		{
			return _BrowseButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = BrowseButton_Click;
			Button val = _BrowseButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_BrowseButton = value;
			val = _BrowseButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button HelpButton1
	{
		[CompilerGenerated]
		get
		{
			return _HelpButton1;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = HelpButton1_Click;
			Button val = _HelpButton1;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_HelpButton1 = value;
			val = _HelpButton1;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button AllButton
	{
		[CompilerGenerated]
		get
		{
			return _AllButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = AllButton_Click;
			Button val = _AllButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_AllButton = value;
			val = _AllButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("SymbolTextBox")]
	internal virtual TextBox SymbolTextBox
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button StartButton
	{
		[CompilerGenerated]
		get
		{
			return _StartButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StartButton_Click;
			Button val = _StartButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StartButton = value;
			val = _StartButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
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

	[field: AccessedThroughProperty("ErrorLabel")]
	internal virtual Label ErrorLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button StopButton
	{
		[CompilerGenerated]
		get
		{
			return _StopButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = StopButton_Click;
			Button val = _StopButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_StopButton = value;
			val = _StopButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	[field: AccessedThroughProperty("DataGridView1")]
	internal virtual DataGridView DataGridView1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("ProgressBar1")]
	internal virtual ProgressBar ProgressBar1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("SymbolLabel")]
	internal virtual Label SymbolLabel
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	[field: AccessedThroughProperty("FolderBrowserDialog1")]
	internal virtual FolderBrowserDialog FolderBrowserDialog1
	{
		get; [MethodImpl(MethodImplOptions.Synchronized)]
		set;
	}

	internal virtual Button ClipboardButton
	{
		[CompilerGenerated]
		get
		{
			return _ClipboardButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = ClipboardButton_Click;
			Button val = _ClipboardButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_ClipboardButton = value;
			val = _ClipboardButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	internal virtual Button PortfolioButton
	{
		[CompilerGenerated]
		get
		{
			return _PortfolioButton;
		}
		[MethodImpl(MethodImplOptions.Synchronized)]
		[CompilerGenerated]
		set
		{
			EventHandler eventHandler = PortfolioButton_Click;
			Button val = _PortfolioButton;
			if (val != null)
			{
				((Control)val).Click -= eventHandler;
			}
			_PortfolioButton = value;
			val = _PortfolioButton;
			if (val != null)
			{
				((Control)val).Click += eventHandler;
			}
		}
	}

	public AnalyzeForm()
	{
		//IL_000e: Unknown result type (might be due to invalid IL or missing references)
		//IL_0018: Expected O, but got Unknown
		((Form)this).FormClosing += new FormClosingEventHandler(AnalyzeForm_FormClosing);
		((Form)this).Load += AnalyzeForm_Load;
		StopPressed = false;
		YAHOOURLeod = "https://query1.finance.yahoo.com/v7/finance/quote?symbols=";
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
		//IL_0064: Unknown result type (might be due to invalid IL or missing references)
		//IL_006e: Expected O, but got Unknown
		//IL_006f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0079: Expected O, but got Unknown
		//IL_007a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0084: Expected O, but got Unknown
		//IL_0085: Unknown result type (might be due to invalid IL or missing references)
		//IL_008f: Expected O, but got Unknown
		//IL_0090: Unknown result type (might be due to invalid IL or missing references)
		//IL_009a: Expected O, but got Unknown
		//IL_009b: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a5: Expected O, but got Unknown
		ListBox1 = new ListBox();
		BrowseButton = new Button();
		HelpButton1 = new Button();
		AllButton = new Button();
		SymbolTextBox = new TextBox();
		StartButton = new Button();
		DoneButton = new Button();
		ErrorLabel = new Label();
		StopButton = new Button();
		DataGridView1 = new DataGridView();
		ProgressBar1 = new ProgressBar();
		SymbolLabel = new Label();
		FolderBrowserDialog1 = new FolderBrowserDialog();
		ClipboardButton = new Button();
		PortfolioButton = new Button();
		((ISupportInitialize)DataGridView1).BeginInit();
		((Control)this).SuspendLayout();
		((Control)ListBox1).Anchor = (AnchorStyles)15;
		ListBox1.HorizontalScrollbar = true;
		((Control)ListBox1).Location = new Point(12, 12);
		ListBox1.MultiColumn = true;
		((Control)ListBox1).Name = "ListBox1";
		ListBox1.SelectionMode = (SelectionMode)3;
		((Control)ListBox1).Size = new Size(894, 186);
		ListBox1.Sorted = true;
		((Control)ListBox1).TabIndex = 2;
		((Control)BrowseButton).Anchor = (AnchorStyles)10;
		((Control)BrowseButton).Location = new Point(846, 321);
		((Control)BrowseButton).Name = "BrowseButton";
		((Control)BrowseButton).Size = new Size(60, 23);
		((Control)BrowseButton).TabIndex = 9;
		((ButtonBase)BrowseButton).Text = "&Browse";
		((ButtonBase)BrowseButton).UseVisualStyleBackColor = true;
		((Control)HelpButton1).Anchor = (AnchorStyles)10;
		((Control)HelpButton1).Location = new Point(846, 292);
		((Control)HelpButton1).Name = "HelpButton1";
		((Control)HelpButton1).Size = new Size(60, 23);
		((Control)HelpButton1).TabIndex = 8;
		((ButtonBase)HelpButton1).Text = "&Help";
		((ButtonBase)HelpButton1).UseVisualStyleBackColor = true;
		((Control)AllButton).Anchor = (AnchorStyles)10;
		((Control)AllButton).Location = new Point(846, 379);
		((Control)AllButton).Name = "AllButton";
		((Control)AllButton).Size = new Size(60, 23);
		((Control)AllButton).TabIndex = 11;
		((ButtonBase)AllButton).Text = "&Select All";
		((ButtonBase)AllButton).UseVisualStyleBackColor = true;
		((Control)SymbolTextBox).Anchor = (AnchorStyles)10;
		((Control)SymbolTextBox).Location = new Point(846, 267);
		((Control)SymbolTextBox).Name = "SymbolTextBox";
		((Control)SymbolTextBox).Size = new Size(60, 20);
		((Control)SymbolTextBox).TabIndex = 7;
		((Control)StartButton).Anchor = (AnchorStyles)10;
		((Control)StartButton).Location = new Point(846, 466);
		((Control)StartButton).Name = "StartButton";
		((Control)StartButton).Size = new Size(60, 23);
		((Control)StartButton).TabIndex = 0;
		((ButtonBase)StartButton).Text = "S&tart";
		((ButtonBase)StartButton).UseVisualStyleBackColor = true;
		((Control)DoneButton).Anchor = (AnchorStyles)10;
		DoneButton.DialogResult = (DialogResult)2;
		((Control)DoneButton).Location = new Point(846, 495);
		((Control)DoneButton).Name = "DoneButton";
		((Control)DoneButton).Size = new Size(60, 23);
		((Control)DoneButton).TabIndex = 1;
		((ButtonBase)DoneButton).Text = "&Done";
		((ButtonBase)DoneButton).UseVisualStyleBackColor = true;
		((Control)ErrorLabel).Anchor = (AnchorStyles)10;
		ErrorLabel.BorderStyle = (BorderStyle)2;
		ErrorLabel.FlatStyle = (FlatStyle)0;
		((Control)ErrorLabel).ForeColor = Color.Red;
		((Control)ErrorLabel).Location = new Point(12, 495);
		((Control)ErrorLabel).Name = "ErrorLabel";
		((Control)ErrorLabel).Size = new Size(405, 21);
		((Control)ErrorLabel).TabIndex = 4;
		ErrorLabel.TextAlign = (ContentAlignment)32;
		((Control)StopButton).Anchor = (AnchorStyles)10;
		((Control)StopButton).Enabled = false;
		((Control)StopButton).Location = new Point(846, 437);
		((Control)StopButton).Name = "StopButton";
		((Control)StopButton).Size = new Size(60, 23);
		((Control)StopButton).TabIndex = 13;
		((ButtonBase)StopButton).Text = "St&op";
		((ButtonBase)StopButton).UseVisualStyleBackColor = true;
		DataGridView1.AllowUserToAddRows = false;
		DataGridView1.AllowUserToDeleteRows = false;
		DataGridView1.AllowUserToResizeColumns = false;
		DataGridView1.AllowUserToResizeRows = false;
		((Control)DataGridView1).Anchor = (AnchorStyles)14;
		DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)10;
		DataGridView1.AutoSizeRowsMode = (DataGridViewAutoSizeRowsMode)11;
		((Control)DataGridView1).CausesValidation = false;
		DataGridView1.ColumnHeadersHeightSizeMode = (DataGridViewColumnHeadersHeightSizeMode)2;
		DataGridView1.EditMode = (DataGridViewEditMode)4;
		((Control)DataGridView1).Location = new Point(12, 204);
		((Control)DataGridView1).Name = "DataGridView1";
		DataGridView1.ReadOnly = true;
		DataGridView1.RowTemplate.ReadOnly = true;
		DataGridView1.RowTemplate.Resizable = (DataGridViewTriState)1;
		DataGridView1.SelectionMode = (DataGridViewSelectionMode)1;
		DataGridView1.ShowCellErrors = false;
		DataGridView1.ShowCellToolTips = false;
		DataGridView1.ShowEditingIcon = false;
		DataGridView1.ShowRowErrors = false;
		((Control)DataGridView1).Size = new Size(824, 285);
		((Control)DataGridView1).TabIndex = 3;
		((Control)ProgressBar1).Anchor = (AnchorStyles)10;
		((Control)ProgressBar1).ForeColor = Color.Green;
		((Control)ProgressBar1).Location = new Point(431, 495);
		((Control)ProgressBar1).Name = "ProgressBar1";
		((Control)ProgressBar1).Size = new Size(405, 21);
		((Control)ProgressBar1).TabIndex = 5;
		((Control)SymbolLabel).Anchor = (AnchorStyles)10;
		((Control)SymbolLabel).Location = new Point(846, 205);
		((Control)SymbolLabel).Name = "SymbolLabel";
		((Control)SymbolLabel).Size = new Size(65, 59);
		((Control)SymbolLabel).TabIndex = 6;
		SymbolLabel.Text = "&New symbol(s), space separated";
		((Control)ClipboardButton).Anchor = (AnchorStyles)10;
		((Control)ClipboardButton).Enabled = false;
		((Control)ClipboardButton).Location = new Point(846, 408);
		((Control)ClipboardButton).Name = "ClipboardButton";
		((Control)ClipboardButton).Size = new Size(60, 23);
		((Control)ClipboardButton).TabIndex = 12;
		((ButtonBase)ClipboardButton).Text = "&Clipboard";
		((ButtonBase)ClipboardButton).UseVisualStyleBackColor = true;
		((Control)PortfolioButton).Anchor = (AnchorStyles)10;
		((Control)PortfolioButton).CausesValidation = false;
		((Control)PortfolioButton).Enabled = false;
		((Control)PortfolioButton).Location = new Point(846, 350);
		((Control)PortfolioButton).Name = "PortfolioButton";
		((Control)PortfolioButton).Size = new Size(60, 23);
		((Control)PortfolioButton).TabIndex = 10;
		((ButtonBase)PortfolioButton).Text = "&Portfolio";
		((ButtonBase)PortfolioButton).UseVisualStyleBackColor = true;
		((Form)this).AcceptButton = (IButtonControl)(object)StartButton;
		((ContainerControl)this).AutoScaleDimensions = new SizeF(6f, 13f);
		((ContainerControl)this).AutoScaleMode = (AutoScaleMode)1;
		((Form)this).AutoScroll = true;
		((Form)this).CancelButton = (IButtonControl)(object)DoneButton;
		((Form)this).ClientSize = new Size(918, 528);
		((Control)this).Controls.Add((Control)(object)PortfolioButton);
		((Control)this).Controls.Add((Control)(object)ClipboardButton);
		((Control)this).Controls.Add((Control)(object)SymbolLabel);
		((Control)this).Controls.Add((Control)(object)ProgressBar1);
		((Control)this).Controls.Add((Control)(object)DataGridView1);
		((Control)this).Controls.Add((Control)(object)StopButton);
		((Control)this).Controls.Add((Control)(object)ErrorLabel);
		((Control)this).Controls.Add((Control)(object)BrowseButton);
		((Control)this).Controls.Add((Control)(object)HelpButton1);
		((Control)this).Controls.Add((Control)(object)AllButton);
		((Control)this).Controls.Add((Control)(object)SymbolTextBox);
		((Control)this).Controls.Add((Control)(object)StartButton);
		((Control)this).Controls.Add((Control)(object)DoneButton);
		((Control)this).Controls.Add((Control)(object)ListBox1);
		((Control)this).Name = "AnalyzeForm";
		((Form)this).StartPosition = (FormStartPosition)4;
		((Form)this).Text = "Analyze Form";
		((ISupportInitialize)DataGridView1).EndInit();
		((Control)this).ResumeLayout(false);
		((Control)this).PerformLayout();
	}

	private void AnalyzeForm_FormClosing(object sender, FormClosingEventArgs e)
	{
	}

	private void AnalyzeForm_Load(object sender, EventArgs e)
	{
		//IL_0000: Unknown result type (might be due to invalid IL or missing references)
		//IL_0005: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_001b: Unknown result type (might be due to invalid IL or missing references)
		//IL_0026: Unknown result type (might be due to invalid IL or missing references)
		//IL_002d: Unknown result type (might be due to invalid IL or missing references)
		//IL_003e: Unknown result type (might be due to invalid IL or missing references)
		//IL_004f: Unknown result type (might be due to invalid IL or missing references)
		//IL_0060: Unknown result type (might be due to invalid IL or missing references)
		//IL_0071: Unknown result type (might be due to invalid IL or missing references)
		//IL_0082: Unknown result type (might be due to invalid IL or missing references)
		//IL_0093: Unknown result type (might be due to invalid IL or missing references)
		//IL_00a4: Unknown result type (might be due to invalid IL or missing references)
		//IL_00b5: Unknown result type (might be due to invalid IL or missing references)
		//IL_00c6: Unknown result type (might be due to invalid IL or missing references)
		ToolTip val = new ToolTip
		{
			AutoPopDelay = 5000,
			InitialDelay = 1000,
			ReshowDelay = 500,
			ShowAlways = true
		};
		val.SetToolTip((Control)(object)AllButton, "Select all of the symbols listed.");
		val.SetToolTip((Control)(object)BrowseButton, "Locate files containing stock quotes for use by Patternz.");
		val.SetToolTip((Control)(object)ClipboardButton, "Copy highlighted rows to the clipboard.");
		val.SetToolTip((Control)(object)DataGridView1, "Results are displayed here.");
		val.SetToolTip((Control)(object)DoneButton, "Exit the form.");
		val.SetToolTip((Control)(object)HelpButton1, "Get help.");
		val.SetToolTip((Control)(object)ListBox1, "Quote files appear here, if any.");
		val.SetToolTip((Control)(object)PortfolioButton, "Select a portfolio to analyze.");
		val.SetToolTip((Control)(object)StartButton, "Begin analyze quote files.");
		val.SetToolTip((Control)(object)StopButton, "Halt the analysis.");
		val.SetToolTip((Control)(object)SymbolTextBox, "Enter new symbol(s) to analyze, each separated by a comma, then click Start.");
		SymbolTextBox.Text = "";
		ListBox ListBox = ListBox1;
		GlobalForm.DisplayFiles(ref ListBox);
		ListBox1 = ListBox;
		((Control)AllButton).Enabled = Conversions.ToBoolean(Interaction.IIf(ListBox1.Items.Count > 0, (object)true, (object)false));
		((Control)PortfolioButton).Enabled = true;
		DataGridView1.ClipboardCopyMode = (DataGridViewClipboardCopyMode)2;
		BuildGridHeader();
	}

	private void AllButton_Click(object sender, EventArgs e)
	{
		ListBox1.BeginUpdate();
		checked
		{
			int num = ListBox1.Items.Count - 1;
			for (int i = 0; i <= num; i++)
			{
				ListBox1.SetSelected(i, true);
			}
			ListBox1.EndUpdate();
		}
	}

	private void BrowseButton_Click(object sender, EventArgs e)
	{
		//IL_0001: Unknown result type (might be due to invalid IL or missing references)
		//IL_0006: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Expected O, but got Unknown
		//IL_001c: Unknown result type (might be due to invalid IL or missing references)
		//IL_0022: Invalid comparison between Unknown and I4
		FolderBrowserDialog1 = new FolderBrowserDialog
		{
			Description = "Select the path to the stock quote files."
		};
		if ((int)((CommonDialog)FolderBrowserDialog1).ShowDialog() == 1)
		{
			GlobalForm.PathChanged = true;
			GlobalForm.OpenPath = FolderBrowserDialog1.SelectedPath;
			ListBox ListBox = ListBox1;
			GlobalForm.DisplayFiles(ref ListBox);
			ListBox1 = ListBox;
			((Control)AllButton).Enabled = Conversions.ToBoolean(Interaction.IIf(ListBox1.Items.Count > 0, (object)true, (object)false));
		}
		ErrorLabel.Text = "File location: " + GlobalForm.OpenPath;
	}

	private void DoneButton_Click(object sender, EventArgs e)
	{
		((Form)this).Close();
	}

	private void StartButton_Click(object sender, EventArgs e)
	{
		//IL_0041: Unknown result type (might be due to invalid IL or missing references)
		//IL_0097: Unknown result type (might be due to invalid IL or missing references)
		//IL_009d: Invalid comparison between Unknown and I4
		//IL_0314: Unknown result type (might be due to invalid IL or missing references)
		if ((ListBox1.Items.Count == 0) & (Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0))
		{
			MessageBox.Show("Please enter one or more symbols into the text box (each of them separated by a space) then click Start.", "Analyze: StartButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
			((Control)SymbolTextBox).Focus();
			return;
		}
		int count = ListBox1.SelectedIndices.Count;
		if (Operators.CompareString(Strings.Trim(SymbolTextBox.Text), "", false) == 0 && count == 0)
		{
			if ((int)MessageBox.Show("No symbols have been selected in the listbox. Did you want me to select them all?", "Analyze: StartButton_Click", (MessageBoxButtons)4, (MessageBoxIcon)32) != 6)
			{
				return;
			}
			AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
			count = ListBox1.SelectedIndices.Count;
		}
		checked
		{
			string[] array;
			if (Operators.CompareString(SymbolTextBox.Text, "", false) != 0)
			{
				array = Strings.Split(Strings.Trim(SymbolTextBox.Text), " ", -1, (CompareMethod)0);
				count = 0;
				int num = array.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					if (Operators.CompareString(array[i], "", false) != 0)
					{
						array[count] = array[i];
						count++;
					}
				}
				if (ListBox1.SelectedIndices.Count > 0)
				{
					array = (string[])Utils.CopyArray((Array)array, (Array)new string[count - 1 + ListBox1.SelectedIndices.Count + 1]);
					int num2 = count;
					int num3 = array.Length - 1;
					for (int i = num2; i <= num3; i++)
					{
						string text = ListBox1.SelectedItems[i - count].ToString();
						array[i] = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
					}
					count = array.Length;
				}
			}
			else
			{
				array = new string[count - 1 + 1];
				int num4 = count - 1;
				for (int i = 0; i <= num4; i++)
				{
					string text = ListBox1.SelectedItems[i].ToString();
					array[i] = Strings.Left(text, Strings.InStrRev(text, ".", -1, (CompareMethod)0) - 1);
				}
			}
			StopPressed = false;
			((Control)AllButton).Enabled = false;
			((Control)BrowseButton).Enabled = false;
			((Control)ClipboardButton).Enabled = false;
			((Control)DoneButton).Enabled = false;
			((Control)HelpButton1).Enabled = false;
			((Control)PortfolioButton).Enabled = false;
			((Control)StartButton).Enabled = false;
			((Control)StopButton).Enabled = true;
			((Control)SymbolTextBox).Enabled = false;
			ProgressBar1.Value = 0;
			DataGridView1.RowCount = 0;
			GetAnalylitics(array);
			((Control)StopButton).Enabled = false;
			((Control)StartButton).Enabled = true;
			((Control)PortfolioButton).Enabled = true;
			((Control)HelpButton1).Enabled = true;
			((Control)DoneButton).Enabled = true;
			((Control)BrowseButton).Enabled = true;
			((Control)ClipboardButton).Enabled = true;
			((Control)AllButton).Enabled = true;
			((Control)SymbolTextBox).Enabled = true;
			ProgressBar1.Value = 100;
			MessageBox.Show("Done", "AnalyzeForm: StartButton_Click", (MessageBoxButtons)0, (MessageBoxIcon)64);
			ProgressBar1.Value = 0;
		}
	}

	public void GetAnalylitics(string[] SymbolArray)
	{
		//IL_0061: Unknown result type (might be due to invalid IL or missing references)
		while (Operators.CompareString(Token.Cookie, "", false) == 0 || Operators.CompareString(Token.Crumb, "", false) == 0)
		{
			Token.Refresh();
			if ((Operators.CompareString(Token.Cookie, "-1", false) == 0) & (Operators.CompareString(Token.Crumb, "-1", false) == 0))
			{
				Token.Cookie = "";
				Token.Crumb = "";
				if (!GlobalForm.Quiet)
				{
					MessageBox.Show("The internet (or yahoo only) may be down.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
				}
				return;
			}
		}
		int iRow = 0;
		string text = "&f=a2b4ee8jkl1j1p5rr5sy";
		int num = SymbolArray.Length;
		checked
		{
			while (!StopPressed)
			{
				int num2 = Conversions.ToInteger(Interaction.IIf(num > 195, (object)195, (object)num));
				string text2 = "";
				int num3 = num2 - 1;
				for (int i = 0; i <= num3; i++)
				{
					text2 = text2 + SymbolArray[num - 1 - i] + Conversions.ToString(Interaction.IIf(i != num2 - 1, (object)"+", (object)""));
				}
				string text3 = null;
				StreamReader streamReader = null;
				Stream stream = null;
				WebResponse webResponse = null;
				try
				{
					string address = YAHOOURLeod + text2 + text + "&crumb=" + Token.Crumb;
					if ((Operators.CompareString(Token.Cookie, "", false) == 0) | (Operators.CompareString(Token.Crumb, "", false) == 0))
					{
						break;
					}
					using WebClient webClient = new WebClient();
					webClient.Headers.Add(HttpRequestHeader.Cookie, Token.Cookie);
					webClient.DownloadString(address);
				}
				catch (WebException ex)
				{
					ProjectData.SetProjectError((Exception)ex);
					WebException ex2 = ex;
					ProjectData.ClearProjectError();
				}
				catch (Exception ex3)
				{
					ProjectData.SetProjectError(ex3);
					Exception ex4 = ex3;
					ProjectData.ClearProjectError();
				}
				ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
				try
				{
					webResponse = WebRequest.CreateHttp(YAHOOURLeod + text2 + text).GetResponse();
					stream = webResponse.GetResponseStream();
					streamReader = new StreamReader(stream);
					text3 = streamReader.ReadToEnd();
					streamReader.Close();
					stream.Close();
					webResponse.Close();
					ParseBuffer(text3, ref iRow);
				}
				catch (Exception ex5)
				{
					ProjectData.SetProjectError(ex5);
					Exception ex6 = ex5;
					HandleInternetException(ex6, GlobalForm.CurrentSymbol);
					streamReader?.Close();
					stream?.Close();
					webResponse?.Close();
					ProjectData.ClearProjectError();
				}
				((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
				if (!StopPressed)
				{
					num -= num2;
					if (num <= 0)
					{
						break;
					}
					continue;
				}
				break;
			}
		}
	}

	private void ParseBuffer(string Buffer, ref int iRow)
	{
		string eOLCode = GetEOLCode(Buffer);
		if (Operators.CompareString(eOLCode, (string)null, false) == 0)
		{
			return;
		}
		checked
		{
			int num = Strings.InStr(Buffer, eOLCode, (CompareMethod)0) + eOLCode.Length;
			string text = Strings.Left(Buffer, num - 1);
			string text2 = GlobalForm.ClosestDelimiter(text);
			if (Operators.CompareString(text2, "-1", false) == 0)
			{
				return;
			}
			DataGridView1.RowHeadersVisible = false;
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)1;
			while (true)
			{
				string[] array = Regex.Split(text, text2);
				DataGridView1.Rows.Add();
				DataGridView1.Rows[iRow].Cells[2].Value = CheckString(array[0]);
				DataGridView1.Rows[iRow].Cells[9].Value = CheckString(array[1]);
				DataGridView1.Rows[iRow].Cells[7].Value = CheckString(array[2]);
				DataGridView1.Rows[iRow].Cells[8].Value = CheckString(array[3]);
				DataGridView1.Rows[iRow].Cells[5].Value = CheckString(array[4]);
				DataGridView1.Rows[iRow].Cells[4].Value = CheckString(array[5]);
				DataGridView1.Rows[iRow].Cells[1].Value = CheckString(array[6]);
				if (Strings.InStr(array[7], "N/A", (CompareMethod)0) != 0)
				{
					DataGridView1.Rows[iRow].Cells[6].Value = "";
				}
				else
				{
					DataGridView1.Rows[iRow].Cells[6].Value = GetMarketCap(array[7]);
				}
				DataGridView1.Rows[iRow].Cells[11].Value = CheckString(array[8]);
				DataGridView1.Rows[iRow].Cells[10].Value = CheckString(array[9]);
				DataGridView1.Rows[iRow].Cells[12].Value = CheckString(array[10]);
				DataGridView1.Rows[iRow].Cells[0].Value = array[11].Replace("\"", "");
				if (Operators.CompareString(Strings.Right(array[12], 1), eOLCode, false) == 0)
				{
					array[12] = Strings.Left(array[12], array[12].Length - eOLCode.Length);
				}
				DataGridView1.Rows[iRow].Cells[3].Value = CheckString(array[12]);
				iRow++;
				if (Buffer.Length - num <= eOLCode.Length)
				{
					break;
				}
				Buffer = Strings.Right(Buffer, Buffer.Length - (num - eOLCode.Length));
				num = Strings.InStr(Buffer, eOLCode, (CompareMethod)0) + eOLCode.Length;
				if (num <= eOLCode.Length)
				{
					break;
				}
				text = Strings.Left(Buffer, num - 1);
				if (unchecked(iRow % 50) == 0)
				{
					((WindowsFormsApplicationBase)MyProject.Application).DoEvents();
					if (StopPressed)
					{
						break;
					}
				}
			}
			DataGridView1.AutoSizeColumnsMode = (DataGridViewAutoSizeColumnsMode)6;
			DataGridView1.RowHeadersVisible = true;
		}
	}

	private void BuildGridHeader()
	{
		DataGridView1.RowCount = 0;
		DataGridView1.ColumnCount = 13;
		DataGridView1.Columns[0].Name = "Symbol";
		DataGridView1.Columns[1].Name = "Price";
		DataGridView1.Columns[2].Name = "Volume";
		DataGridView1.Columns[3].Name = "Yield";
		DataGridView1.Columns[4].Name = "Yr High";
		DataGridView1.Columns[5].Name = "Yr Low";
		DataGridView1.Columns[6].Name = "Market Cap";
		DataGridView1.Columns[7].Name = "Earnings/Sh";
		DataGridView1.Columns[8].Name = "Next Yr EPS?";
		DataGridView1.Columns[9].Name = "Book Value";
		DataGridView1.Columns[10].Name = "P/E";
		DataGridView1.Columns[11].Name = "PSR";
		DataGridView1.Columns[12].Name = "PEG";
	}

	private void HandleInternetException(Exception ex, string Symbol)
	{
		string text = "The remote name could not be resolved";
		if (Strings.InStr(ex.Message, "404", (CompareMethod)0) != 0)
		{
			ErrorLabel.Text = "Bad symbol or quotes not available yet: " + Symbol;
		}
		else if (Strings.InStr(ex.Message, "400", (CompareMethod)0) != 0)
		{
			ErrorLabel.Text = "Bad symbol? " + Symbol;
		}
		else if (Operators.CompareString(Strings.Left(ex.Message, text.Length), text, false) == 0)
		{
			ErrorLabel.Text = "No internet connection. Is security software blocking access?";
		}
		else
		{
			ErrorLabel.Text = ex.Message;
		}
	}

	private string GetEOLCode(string Buffer)
	{
		string text = "\r\n";
		while (true)
		{
			if (Strings.InStr(Buffer, text, (CompareMethod)0) != 0)
			{
				return text;
			}
			if (Operators.CompareString(text, "\r\n", false) == 0)
			{
				text = "\n";
				continue;
			}
			if (Operators.CompareString(text, "\n", false) != 0)
			{
				break;
			}
			text = "\r";
		}
		return null;
	}

	private void StopButton_Click(object sender, EventArgs e)
	{
		StopPressed = true;
		Interaction.Beep();
	}

	private void HelpButton1_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		((Form)MyProject.Forms.AnalyzeFormHelp).ShowDialog();
	}

	private string GetMarketCap(string MarketCap)
	{
		string text = Strings.UCase(Strings.Right(MarketCap, 1));
		double num = checked((Operators.CompareString(text, "B", false) == 0) ? (Conversion.Val(Strings.Left(MarketCap, MarketCap.Length - 1)) * 1000000000.0) : ((Operators.CompareString(text, "M", false) != 0) ? Conversion.Val(MarketCap) : (Conversion.Val(Strings.Left(MarketCap, MarketCap.Length - 1)) * 1000000.0)));
		double num2 = num;
		if (num2 < 1000000000.0)
		{
			return "Small";
		}
		if (num2 > 5000000000.0)
		{
			return "Large";
		}
		return "Mid";
	}

	private decimal CheckString(string Value)
	{
		decimal result;
		if (Strings.InStr(Value, "N/A", (CompareMethod)0) != 0)
		{
			ErrorLabel.Text = "Row of zeros: website doesn't recognize symbol or data unavailable?";
			result = default(decimal);
		}
		else
		{
			try
			{
				return Conversions.ToDecimal(Value);
			}
			catch (Exception ex)
			{
				ProjectData.SetProjectError(ex);
				Exception ex2 = ex;
				result = default(decimal);
				ProjectData.ClearProjectError();
			}
		}
		return result;
	}

	private void ClipboardButton_Click(object sender, EventArgs e)
	{
		//IL_00fa: Unknown result type (might be due to invalid IL or missing references)
		//IL_003d: Unknown result type (might be due to invalid IL or missing references)
		//IL_0043: Expected O, but got Unknown
		//IL_00d1: Unknown result type (might be due to invalid IL or missing references)
		string text = "";
		if (((BaseCollection)DataGridView1.SelectedRows).Count == 0)
		{
			DataGridView1.SelectAll();
		}
		foreach (DataGridViewColumn item in (BaseCollection)DataGridView1.Columns)
		{
			DataGridViewColumn val = item;
			text = text + val.Name + "\t";
		}
		try
		{
			text += "\r\n";
			Clipboard.SetDataObject((object)DataGridView1.GetClipboardContent());
			text += Clipboard.GetText();
			Clipboard.SetText(text);
			MessageBox.Show("Done! " + ((BaseCollection)DataGridView1.SelectedRows).Count + " rows copied.", "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)64);
		}
		catch (Exception ex)
		{
			ProjectData.SetProjectError(ex);
			Exception ex2 = ex;
			MessageBox.Show("Clipboard is busy with another user. Error: " + ex2.Message, "Patternz", (MessageBoxButtons)0, (MessageBoxIcon)16);
			ProjectData.ClearProjectError();
		}
	}

	private void PortfolioButton_Click(object sender, EventArgs e)
	{
		//IL_000a: Unknown result type (might be due to invalid IL or missing references)
		//IL_0010: Unknown result type (might be due to invalid IL or missing references)
		//IL_0016: Invalid comparison between Unknown and I4
		((Form)MyProject.Forms.PortfolioDialog).ShowDialog();
		if ((int)GlobalForm.CustomResult == 1)
		{
			GlobalForm.OpenPath = GlobalForm.PDSelectionPath;
			ListBox ListBox = ListBox1;
			GlobalForm.DisplayFiles(ref ListBox);
			ListBox1 = ListBox;
			AllButton_Click(RuntimeHelpers.GetObjectValue(sender), e);
		}
	}
}
