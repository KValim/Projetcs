USE [DBDINDIN]
GO

/****** Object:  Table [dbo].[tbProduto]    Script Date: 18/05/2022 12:48:02 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[tbProduto](
	[nomeProduto] [varchar](50) NOT NULL,
	[quantidadeLikes] [int] NULL,
 CONSTRAINT [PK_tbProduto] PRIMARY KEY CLUSTERED 
(
	[nomeProduto] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

