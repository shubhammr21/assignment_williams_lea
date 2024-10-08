<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:leg="http://www.legislation.gov.uk/namespaces/legislation"
                xmlns:atom="http://www.w3.org/2005/Atom"
                xmlns:ukm="http://www.legislation.gov.uk/namespaces/metadata"
                xmlns:dc="http://purl.org/dc/elements/1.1/"
                version="1.0">

    <!-- Template to match the root element -->
    <xsl:template match="/">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
            <title>
                <xsl:value-of select="//dc:title"/>
            </title>
        </head>
        <body>
        <!-- Page Title -->
        <h1 id="pageTitle" class="fw-light mb-4">
            <xsl:value-of select="//dc:title"/>
        </h1>
        <!-- Contents List -->
        <div class="px-5">
            <ul class="list-unstyled">
                <!-- Introduction Section -->
                <li class="LegContentsEntry">
                    <a class="text-decoration-none fw-normal" href="{//ukm:SecondaryPrelims/@DocumentURI}">Introductory
                        Text</a>
                </li>

                <!-- Dynamically Generate List Items from Contents -->
                <xsl:for-each select="//leg:Contents/leg:ContentsItem">
                    <li class="LegContentsEntry">

                        <a class="text-decoration-none fw-normal" href="{@DocumentURI}">
                            <xsl:value-of select="leg:ContentsNumber"/>
                            .
                            <xsl:value-of select="leg:ContentsTitle"/>
                        </a>
                    </li>
                </xsl:for-each>
                <!-- Signature and Note Sections -->
                <li class="LegContentsEntry">
                    <a class="text-decoration-none fw-normal"
                       href="{//atom:link[@title='signature']/@href}">Signature</a>
                </li>
                <li class="LegContentsEntry">
                    <a class="text-decoration-none fw-normal" href="{//atom:link[@title='note']/@href}">Explanatory
                        Note</a>
                </li>
            </ul>
        </div>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
